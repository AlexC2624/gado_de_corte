import os
import subprocess
import requests

class Sincronizar:
    def __init__(self, remote='meudrive', pasta_local='dados', pasta_remota='dados'):
        self.remote = remote
        self.pasta_local = pasta_local
        self.pasta_remota = pasta_remota

    def _executar(self, cmd):
        """Executa o comando em um novo terminal separado

        Args:
            cmd (list[str]): O comando a ser executado.

        Returns:
            dict: Dicionário com 'saida', 'erro' e 'codigo'
        """
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        return {
            'saida': resultado.stdout.strip(),
            'erro': resultado.stderr.strip(),
            'codigo': resultado.returncode
        }
    
    def verificar_conn(self):
        """Verifica se tem conexão com o google

        Returns:
            bool: True se tem conexão ou False.
        """
        try:
            requests.get('https://www.google.com', timeout=5)
            return True
        except requests.ConnectionError: return False

    def push(self):
        """
        Envia arquivos modificados da pasta local para o Google Drive.

        Returns:
            dict: Contém as chaves 'saida' e 'erro'.
        """
        caminho_remoto = f"{self.remote}:/{self.pasta_remota}"
        resultado = self._executar(['rclone', 'sync', self.pasta_local, caminho_remoto])
        return {
            'saida': resultado['saida'],
            'erro': resultado['erro']
        }

    def pull(self):
        """
        Atualiza a pasta local com os dados do Google Drive.

        Returns:
            dict: Contém as chaves 'saida' e 'erro'.
        """
        caminho_remoto = f"{self.remote}:/{self.pasta_remota}"
        resultado = self._executar(['rclone', 'sync', caminho_remoto, self.pasta_local])
        return {
            'saida': resultado['saida'],
            'erro': resultado['erro']
        }

    def teve_mudanca(self):
        """
        Verifica se há alterações entre a pasta local e a remota.

        Returns:
            dict: {
                'local': True se há mudanças locais,
                'remoto': True se há mudanças no remoto
            }
        """
        caminho_remoto = f"{self.remote}:/{self.pasta_remota}"

        # Checa diferenças locais (arquivos na local que não estão no remoto)
        check_local = self._executar(['rclone', 'check', self.pasta_local, caminho_remoto, '--one-way'])
        mudanca_local = check_local['codigo'] != 0

        # Checa diferenças remotas (arquivos no remoto que não estão no local)
        check_remoto = self._executar(['rclone', 'check', caminho_remoto, self.pasta_local, '--one-way'])
        mudanca_remota = check_remoto['codigo'] != 0

        return {
            'local': mudanca_local,
            'remoto': mudanca_remota
        }

    def start(self):
        if self.verificar_conn():
            print('Sincronizando dados...')
            mudanca = self.teve_mudanca()
            if mudanca['local']:
                print(self.push())
                return True, 'Dados locais enviados com sucesso '
            if mudanca['remoto']:
                self.pull()
                return True, 'Dados remotos recebidos com sucesso '
            return True, 'Os dados já estão atualizados '
        else: return False, 'Trabalhando off-line '


if __name__ == '__main__':
    s = Sincronizar()
    print(s.start()[1])
