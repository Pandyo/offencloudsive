resource "aws_instance" "ec2" {
  ami                       = "ami-0a463f27534bdf246" #ami 이름 (지역별로 고유)
  instance_type             = "t3.micro"
  subnet_id                 = var.public_subnet_id_01 #퍼블릭 서브넷 id
  vpc_security_group_ids    = [var.security_group_id] #보안 그룹 id
  associate_public_ip_address = true

  root_block_device { #스토리지
    volume_size           = 8 #볼륨 크기
    volume_type           = "gp3" #볼륨 유형
    iops                  = 3000 #프로비저닝된 iops 값
    delete_on_termination = true #인스턴스 종료 시 삭제 여부
    encrypted             = true #암호화 여부
    kms_key_id            = "alias/aws/ebs" #기본값 aws/ebs 키 사용
    throughput            = 125 #처리량
  }

  instance_initiated_shutdown_behavior = "stop"

  metadata_options { #인스턴스 메타데이터 옵션
    http_endpoint               = "enabled" #메타데이터 액세스 기능 활성화
    http_protocol_ipv6          = "disabled" #메타데이터 IPv6 비활성화
    http_tokens                 = "optional" 
    http_put_response_hop_limit = 1 #홉 수 제한
    instance_metadata_tags      = "enabled" #메타데이터에서 인스턴스 태그 접근 활성화
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y python3 python3-venv python3-pip nginx

              mkdir -p /opt/flaskapp
              cat > /opt/flaskapp/app.py << 'PYCODE'
              ${file("${path.module}/app/app.py")}
              PYCODE

              cat > /opt/flaskapp/requirements.txt << 'REQ'
              ${file("${path.module}/app/requirements.txt")}
              REQ

              cd /opt/flaskapp
              python3 -m venv venv
              source venv/bin/activate
              pip install -r requirements.txt
              nohup venv/bin/python3 app.py &
              EOF
}
