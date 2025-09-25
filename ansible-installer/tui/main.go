package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/bubbles/checkbox"
	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/progress"
	"github.com/charmbracelet/bubbles/spinner"
	"github.com/charmbracelet/bubbles/table"
	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	"github.com/charmbracelet/lipgloss"
	"github.com/go-git/go-git/v5"
	"github.com/google/go-github/v62/github"
	"github.com/otiai10/copy"
	"golang.org/x/oauth2"
)

type model struct {
	choices     []string
	checkboxes  checkbox.Model
	cursor      int
	progress    progress.Model
	spinner     spinner.Model
	viewport    viewport.Model
	textinput   textinput.Model
	aiSuggestion string
	plugins     []string
	scripts     []string
	installing  bool
	percentage  float64
	githubClient *github.Client
	err         error
	width       int
	height      int
}

var (
	softwareList = []string{
		"Node.js", "PNPM", "PostgreSQL", "Supabase", "Ollama", "LocalAI", "OpenWebUI", "LiteLLM", "Forgejo", "Tailscale", "ZeroTier",
		"Prometheus", "Grafana", "RabbitMQ", "Neo4j", "LocalRecall", "Fluentd", "Kong", "Traefik",
	}

	// Key bindings
	enterKey = key.NewBinding(key.WithKeys("enter"))
	upKey    = key.NewBinding(key.WithKeys("up", "k"))
	downKey  = key.NewBinding(key.WithKeys("down", "j"))
	aiKey    = key.NewBinding(key.WithKeys("a")) // AI suggestion
	gitKey   = key.NewBinding(key.WithKeys("g")) // GitHub fetch
	plugKey  = key.NewBinding(key.WithKeys("p")) // Plugins
)

func initialModel() model {
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))

	checkboxes := checkbox.DefaultMulti()
	for _, choice := range softwareList {
		checkboxes.AddItem(choice, false)
	}

	progress := progress.New(progress.WithScale(progress.NewScale(200)))
	progress.Width = 50
	progress.Style = lipgloss.NewStyle().
		Foreground(lipgloss.Color("63")).
		Background(lipgloss.Color("237")).
		Padding(0, 2)

	ti := textinput.New()
	ti.Placeholder = "Search or AI prompt..."
	ti.CharLimit = 156
	ti.Width = 50

	vp := viewport.New(80, 20)
	vp.MouseWheelEnabled = true

	// GitHub client (use token from env)
	var client *github.Client
	if token := os.Getenv("GITHUB_TOKEN"); token != "" {
		ts := oauth2.StaticTokenSource(&oauth2.Token{AccessToken: token})
		tc := oauth2.NewClient(oauth2.NoContext, ts)
		client = github.NewClient(tc)
	}

	return model{
		choices:     softwareList,
		checkboxes:  checkboxes,
		progress:    progress,
		spinner:     s,
		viewport:    vp,
		textinput:   ti,
		aiSuggestion: "AI ready: Ask for install suggestions...",
		plugins:     []string{"litellm", "ollama", "localai"},
		scripts:     []string{"cloudcurio_worker_install.sh", "bootstrap.sh"}, // From local/remote
		installing:  false,
		percentage:  0,
		githubClient: client,
	}
}

func (m model) Init() tea.Cmd {
	return tea.Batch(
		m.spinner.Tick,
		m.fetchGitHubInspo, // Fetch top Bubble Tea repos
		m.loadScripts,      // Load from local/remote
	)
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		m.progress.Width = msg.Width - 4
		m.viewport.Width = msg.Width
		m.viewport.Height = msg.Height - 10
		m.textinput.Width = msg.Width - 4

	case tea.KeyMsg:
		switch {
		case key.Matches(msg, enterKey):
			if m.installing {
				m.installing = false
				return m, nil
			}
			// Install selected
			selected := m.checkboxes.Values()
			if len(selected) > 0 {
				m.installing = true
				m.percentage = 0
				cmds = append(cmds, m.startInstall(selected))
			}

		case key.Matches(msg, upKey):
			m.cursor--
			if m.cursor < 0 {
				m.cursor = len(m.choices) - 1
			}

		case key.Matches(msg, downKey):
			m.cursor++
			if m.cursor >= len(m.choices) {
				m.cursor = 0
			}

		case key.Matches(msg, aiKey):
			// AI integration: Call Ollama/LocalAI via LiteLLM
			prompt := m.textinput.Value()
			if prompt != "" {
				suggestion, err := m.getAISuggestion(prompt)
				if err != nil {
					m.err = err
				} else {
					m.aiSuggestion = suggestion
				}
			}

		case key.Matches(msg, gitKey):
			// GitHub integration: Fetch/pull updates or inspo
			cmds = append(cmds, m.fetchGitHubInspo())

		case key.Matches(msg, plugKey):
			// Plugins: List/load
			m.viewport.SetContent(m.renderPlugins())

		default:
			var cmd tea.Cmd
			m.textinput, cmd = m.textinput.Update(msg)
			cmds = append(cmds, cmd)
		}

	case spinner.TickMsg:
		var cmd tea.Cmd
		m.spinner, cmd = m.spinner.Update(msg)
		cmds = append(cmds, cmd)

	case progress.FrameMsg:
		progress, cmd := m.progress.Update(msg)
		m.progress = progress
		cmds = append(cmds, cmd)

	case installProgressMsg:
		m.percentage = msg.percentage
		if m.percentage >= 100 {
			m.installing = false
			m.percentage = 0
		}
		m.progress.SetPercent(m.percentage / 100)

	case errorMsg:
		m.err = msg.err

	case githubInspoMsg:
		m.viewport.SetContent(m.renderInspo(msg.repos))

	case scriptMsg:
		m.scripts = append(m.scripts, msg.script)
	}

	// Checkbox update
	if !m.installing {
		_, cmd := m.checkboxes.Update(msg)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}

func (m model) View() string {
	if m.width == 0 {
		return "Initializing..."
	}

	header := lipgloss.NewStyle().
		Foreground(lipgloss.Color("205")).
		Background(lipgloss.Color("0")).
		Padding(0, 1).
		Render("CloudCurio TUI Installer")

	// Software table with checkboxes
	columns := []table.Column{
		{Title: "Select", Width: 8},
		{Title: "Software", Width: 20},
		{Title: "Status", Width: 10},
	}
	var rows []table.Row
	for i, choice := range m.choices {
		checked := m.checkboxes.Checked(choice)
		status := "Ready"
		if m.installing && checked {
			status = fmt.Sprintf("%.0f%%", m.percentage)
		}
		rows = append(rows, table.Row{strings.Repeat(" ", 8), choice, status})
	}

	t := table.New(
		table.WithColumns(columns),
		table.WithRows(rows),
		table.WithHeight(m.height-15),
		table.WithFocused(true),
	)
	t.SetCursor(m.cursor)

	tableStyle := lipgloss.NewStyle().
		Border(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		Padding(1, 2)

	// Progress bar
	progressView := m.progress.View()
	if m.installing {
		progressView = m.spinner.View() + " Installing... " + progressView
	}

	// AI Suggestion
	aiView := lipgloss.NewStyle().
		Foreground(lipgloss.Color("212")).
		Render("AI: " + m.aiSuggestion)

	// Plugins and Scripts
	pluginsView := lipgloss.NewStyle().
		Foreground(lipgloss.Color("45")).
		Render(fmt.Sprintf("Plugins (%d): %s | Scripts (%d): %s", len(m.plugins), strings.Join(m.plugins, ", "), len(m.scripts), strings.Join(m.scripts, ", ")))

	// Input
	inputView := m.textinput.View()

	// Viewport for inspo
	inspoView := m.viewport.View()

	// Error
	var errView string
	if m.err != nil {
		errView = lipgloss.NewStyle().
			Foreground(lipgloss.Color("196")).
			Render(fmt.Sprintf("Error: %v", m.err))
	}

	main := lipgloss.JoinVertical(
		lipgloss.Top,
		header,
		tableStyle.Render(t.View()),
		progressView,
		aiView,
		pluginsView,
		inputView,
		inspoView,
		errView,
	)

	return main
}

type installProgressMsg struct{ percentage float64 }
type errorMsg struct{ err error }
type githubInspoMsg struct{ repos []*github.Repository }
type scriptMsg struct{ script string }

func (m model) startInstall(selected []string) tea.Cmd {
	return func() tea.Msg {
		total := len(selected)
		for i, item := range selected {
			// Simulate install (call Ansible or scripts)
			cmd := exec.Command("ansible-playbook", "-i", "inventories/local/hosts.yml", "playbooks/install-all.yml", "--tags", item)
			output, err := cmd.CombinedOutput()
			if err != nil {
				return errorMsg{err}
			}
			perc := float64((i+1)*100) / float64(total)
			time.Sleep(500 * time.Millisecond) // Simulate progress
			return installProgressMsg{perc}
		}
		return installProgressMsg{100}
	}
}

func (m model) getAISuggestion(prompt string) (string, error) {
	// LiteLLM proxy to Ollama/LocalAI
	url := "http://localhost:4000/chat/completions" // LiteLLM
	reqBody := map[string]interface{}{
		"model": "ollama/llama2",
		"messages": []map[string]string{{"role": "user", "content": fmt.Sprintf("Suggest install for: %s in CloudCurio", prompt)}},
	}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := http.Post(url, "application/json", strings.NewReader(string(jsonData)))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(body, &result)
	choices := result["choices"].([]interface{})
	return choices[0].(map[string]interface{})["message"].(map[string]interface{})["content"].(string), nil
}

func (m model) fetchGitHubInspo() tea.Cmd {
	return func() tea.Msg {
		if m.githubClient == nil {
			return errorMsg{fmt.Errorf("No GitHub token")}
		}
		repos, _, err := m.githubClient.Search.Repositories("bubbletea", &github.SearchOptions{
			Sort:  "stars",
			Order: "desc",
			ListOptions: github.ListOptions{PerPage: 10},
		})
		if err != nil {
			return errorMsg{err}
		}
		// Clone top 3 to examples/
		for i, repo := range repos.Repositories[:3] {
			if err := git.PlainClone(os.TempDir()+"/temp-repo", false, &git.CloneOptions{
				URL:   *repo.CloneURL,
				Depth: 1,
			}); err == nil {
				copy.Copy(os.TempDir()+"/temp-repo", fmt.Sprintf("examples/bubbletea-%d", i+1))
			}
		}
		return githubInspoMsg{repos.Repositories}
	}
}

func (m model) loadScripts() tea.Cmd {
	return func() tea.Msg {
		// Local scripts
		files, _ := os.ReadDir("../../scripts")
		for _, f := range files {
			if strings.HasSuffix(f.Name(), ".sh") || strings.HasSuffix(f.Name(), ".py") {
				m.scripts = append(m.scripts, f.Name())
			}
		}
		// Remote (cbwdellr720, Tailscale IP 100.*)
		// Assume scp: scp cbwinslow@100.*.*.*:~/scripts/* . (manual or via exec)
		cmd := exec.Command("scp", "cbwinslow@100.*.*.*:~/scripts/*.sh", ".")
		if err := cmd.Run(); err == nil {
			// Add fetched
		}
		return scriptMsg{"remote_script.sh"} // Placeholder
	}
}

func (m model) renderPlugins() string {
	var s strings.Builder
	for _, p := range m.plugins {
		s.WriteString(p + " ")
	}
	return s.String()
}

func (m model) renderInspo(repos []*github.Repository) string {
	var s strings.Builder
	for _, r := range repos {
		s.WriteString(fmt.Sprintf("- %s/%s (%d stars): %s\n", *r.Owner.Login, *r.Name, *r.StargazersCount, *r.Description))
	}
	return s.String()
}

func main() {
	if _, err := tea.NewProgram(initialModel(), tea.WithAltScreen()).Run(); err != nil {
		log.Fatal(err)
	}
}
