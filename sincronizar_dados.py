import os
import subprocess

class Sincronizar:
    def __init__(self):
        pass

    def _executar(self, cmd):
        """Executa o comando em um novo terminal separado

        Args:
            cmd (list[str]): O comando a ser executado.

        Returns:
            dict: Dicionário com \'saida\', \'erro\' e \'codigo\'
        """
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        resultado = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_dir)
        return {'saida': resultado.stdout.strip(),
                'erro': resultado.stderr.strip(),
                'codigo': resultado.returncode}

    def ver_conn_git(self):
        """Verifica a conexão com o github

        Returns:
            bool: True de tudo der certo, se não False.
        """
        resultado = self._executar(['git', 'fetch'])
        return True if resultado['codigo'] == 0 else False

    def pull(self):
        """Atualiza o repositório local

        Returns:
            dict: Contém 2 chaves \'saida\' e \'erro\'
        """
        saida, erro, _ = self._executar(['git', 'pull'])
        return {'saida': saida, 'erro': erro}
    
    def push(self):
        """
        Adiciona arquivos modificados na pasta 'dados', realiza o commit e envia para o repositório remoto.

        Returns:
            dict: Contém as chaves 'saida' e 'erro'.
        """
        # Verifica alterações na pasta 'dados'
        status = self._executar(['git', 'status', '--porcelain', 'dados'])
        
        # Cada linha do status segue o padrão: "XY caminho/arquivo"
        arquivos_modificados = []
        for linha in status['saida'].splitlines():
            if not linha.strip():
                continue
            partes = linha.strip().split(maxsplit=1)
            if len(partes) == 2:
                arquivos_modificados.append(partes[1])

        if arquivos_modificados:
            # Adiciona os arquivos ao stage
            for arquivo in arquivos_modificados:
                self._executar(['git', 'add', arquivo])

            # Faz o commit
            mensagem = "Atualização automática da pasta 'dados'"
            self._executar(['git', 'commit', '-m', mensagem])

        # Push para o remoto
        resultado = self._executar(['git', 'push'])
        return {
            'saida': resultado['saida'],
            'erro': resultado['erro']
        }
        
    def teve_mudanca(self):
        """
        Verifica se há alterações locais ou se o repositório remoto está diferente do local.

        Retorna:
            dict: {
                'local': True se há mudanças locais na pasta 'dados',
                'remoto': True se há mudanças no repositório remoto não aplicadas localmente
            }
        """
        # Atualiza referências remotas
        self._executar(['git', 'fetch'])

        # Verifica mudanças locais na pasta 'dados'
        status = self._executar(['git', 'status', '--porcelain', 'dados'])
        mudanca_local = bool(status['saida'])

        # Compara o hash local com o remoto
        local = self._executar(['git', 'rev-parse', '@'])
        remoto = self._executar(['git', 'rev-parse', '@{u}'])  # upstream
        base = self._executar(['git', 'merge-base', '@', '@{u}'])

        # Detecta se há commits no remoto ainda não baixados
        mudanca_remota = (remoto['saida'] != base['saida'])

        return {
            'local': mudanca_local,
            'remoto': mudanca_remota
        }

    def start(self):
        print('Sincronizando dados... ')
        if self.ver_conn_git():
            mudanca = self.teve_mudanca()
            if mudanca['local']:
                self.push()
                return True, 'Dados locais enviados com sucesso '
            if mudanca['remoto']:
                self.pull()
                return True, 'Dados remoto recebidos com sucesso '
            return True, 'Os Dados já estão atualizados '
        return False, 'Erro de conexão com o Github '


if __name__ == '__main__':
    s = Sincronizar()
    print(s.start())
