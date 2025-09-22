# Dockerfile for Kali Linux OSINT Tools Container

FROM kalilinux/kali-rolling

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install essential Kali Linux tools for OSINT
RUN apt-get update && apt-get install -y \
    # System tools
    curl \
    wget \
    git \
    nano \
    vim \
    tmux \
    net-tools \
    iputils-ping \
    dnsutils \
    whois \
    nmap \
    # Python and development tools
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    # Web tools
    nikto \
    dirb \
    gobuster \
    whatweb \
    # Network analysis
    tcpdump \
    wireshark \
    tshark \
    # Password auditing
    hydra \
    john \
    # Exploitation tools
    metasploit-framework \
    sqlmap \
    # Social engineering tools
    set \
    # Wireless tools
    aircrack-ng \
    reaver \
    # Forensics tools
    autopsy \
    sleuthkit \
    # Reverse engineering
    gdb \
    radare2 \
    # Reporting tools
    pandoc \
    texlive \
    # Additional useful tools
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install \
    requests \
    beautifulsoup4 \
    lxml \
    selenium \
    scrapy \
    shodan \
    theHarvester \
    sublist3r \
    && rm -rf /root/.cache

# Create working directory
WORKDIR /opt/osint

# Expose ports for common services
EXPOSE 80 443 8080 8443

# Default command
CMD ["/bin/bash"]