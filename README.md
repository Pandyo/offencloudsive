# offencloudsive

## Setting and Start

### install terraform

- linux
```bash
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

- mac os

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

https://developer.hashicorp.com/terraform/install

### install AWS CLI

- linux (amd)
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- linux (arm)
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- mac os
```bash
brew install awscli
```

https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html

### Setting offencloudsive

- git clone offencloudsive
```bash
git clone https://github.com/Pandyo/offencloudsive
```

- aws confingure

Create an Access key in AWS and run the command below to register the Access key, Secret key, and region.
```bash
aws configure --profile offencloudsive
```

### CMD offencloudsive

- start
```bash
python3 offencloudsive.py --scenario scenario_name --profile offencloudsive
```

- destroy
```bash
python3 offencloudsive.py --scenario scenario_name --profile offencloudsive --destroy
```
