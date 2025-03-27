import paramiko as pk
import os

argo_token = os.environ["ARGO_TOKEN"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]


class Keep_serv00:
    _hostname = os.getenv("HOSTNAME", "web12.serv00.com")
    _port = os.getenv("PORT", 22)

    def __init__(self, argo_token, username, password):
        self.argo_token = argo_token
        self.username = username
        self.password = password

    @staticmethod
    def check_process(client, process_name):
        _, stdout, _ = client.exec_command(f"pgrep -x '{process_name}'")

        if stdout.channel.recv_exit_status() == 0:
            print(f"{process_name} is running")

        return stdout.channel.recv_exit_status() == 0

    @staticmethod
    def run_web(client):
        cmd = "nohup /home/$USER/.vmess/web run -c /home/$USER/.vmess/config.json > /home/$USER/.vmess/webtest.log 2>&1 &"
        _, stdout, stderr = client.exec_command(cmd)

        if stdout.channel.recv_exit_status() != 0:
            print(f"Failed to start web: {stderr.read().decode()}")

    @staticmethod
    def run_bot(client):
        cmd = f'nohup /home/$USER/.vmess/bot tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token "{argo_token}" > /home/$USER/.vmess/bottest.log 2>&1 &'
        _, stdout, stderr = client.exec_command(cmd)

        if stdout.channel.recv_exit_status() != 0:
            print(f"Failed to start bot: {stderr.read().decode()}")

    def start(self):
        client = pk.SSHClient()
        client.set_missing_host_key_policy(pk.AutoAddPolicy())

        try:
            client.connect(
                Keep_serv00._hostname,
                Keep_serv00._port,
                self.username,
                self.password,
            )

            if not Keep_serv00.check_process(client, "web"):
                Keep_serv00.run_web(client)

            if not Keep_serv00.check_process(client, "bot"):
                Keep_serv00.run_bot(client)

        except TimeoutError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            client.close()


if __name__ == "__main__":
    k = Keep_serv00(argo_token, username, password)
    k.start()
