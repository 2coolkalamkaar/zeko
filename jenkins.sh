# 1. Update your system's package index
sudo apt update && sudo apt upgrade -y

# 2. Install OpenJDK 21 and fontconfig (Jenkins strictly requires Java 21)
sudo apt install fontconfig openjdk-21-jre -y

# 3. Verify the installation (ensure it outputs version 21)
java -version

# 4. Create the keyrings directory (Modern Ubuntu/Debian security standard)
sudo mkdir -p /etc/apt/keyrings

# 5. Download the newly rotated 2026 Jenkins GPG key
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

# 6. Add the Jenkins stable repository, explicitly pointing to the new key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# 7. Update the package index again to register the new repository
sudo apt update

# 8. Install Jenkins
sudo apt install jenkins -y

# 9. Start the Jenkins service
sudo systemctl start jenkins

# 10. Enable Jenkins to start automatically if the server reboots
sudo systemctl enable jenkins

# 11. Check the status to ensure it is running (look for "active (running)")
sudo systemctl status jenkins



# for password 

sudo cat /var/lib/jenkins/secrets/initialAdminPassword