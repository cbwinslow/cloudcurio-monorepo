# Dockerfile for BlackArch Linux OSINT Tools Container

FROM blackarchlinux/blackarch

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update system and install essential tools
RUN pacman -Syu --noconfirm \
    # System tools
    curl \
    wget \
    git \
    nano \
    vim \
    tmux \
    net-tools \
    iputils \
    dnsutils \
    whois \
    nmap \
    # Python and development tools
    python3 \
    python-pip \
    base-devel \
    # Web tools
    nikto \
    dirb \
    gobuster \
    whatweb \
    # Network analysis
    tcpdump \
    wireshark-cli \
    tshark \
    # Password auditing
    hydra \
    john \
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
    texlive-most \
    # Additional useful tools
    jq \
    && pacman -Scc --noconfirm

# Install Python packages
RUN pip install \
    requests \
    beautifulsoup4 \
    lxml \
    selenium \
    scrapy \
    shodan \
    theHarvester \
    sublist3r \
    && rm -rf /root/.cache

# Install BlackArch tools
RUN pacman -S --noconfirm \
    blackarch-webapp \
    blackarch-recon \
    blackarch-scanner \
    blackarch-exploitation \
    blackarch-sniffer \
    blackarch-socialengineering \
    blackarch-forensic \
    blackarch-reverse \
    blackarch-fuzzer \
    blackarch-crypto \
    blackarch-misc \
    && pacman -Scc --noconfirm

# Create working directory
WORKDIR /opt/osint

# Expose ports for common services
EXPOSE 80 443 8080 8443

# Default command
CMD ["/bin/bash"]