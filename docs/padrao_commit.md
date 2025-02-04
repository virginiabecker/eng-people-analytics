# Padrão de Nomenclatura para Criação de Branches e Commits no GitHub

## 📥 Clonando o Repositório
```bash
git clone https://github.com/eng-pipoca-agil/eng-people-analytics.git
```

---

## 🌿 Padrão de Nomenclatura de Branches
Utilizamos o seguinte padrão para criar e nomear as branches:

### 📌 Categorias:
- `docs/` - Documentação
- `feat/` - Novas funcionalidades
- `fix/` - Correções de bugs
- `test/` - Testes
- `refactor/` - Refatoração de código
- `chore/` - Tarefas de manutenção
- `style/` - Alterações de formatação e estilo
- `perf/` - Melhorias de desempenho
- `ci/` - Integração contínua
- `build/` - Compilação do projeto

### 📌 Exemplo de Nomeação:
```bash
git checkout -b <categoria>/<arquivo_ou_funcionalidade>
```
Exemplo prático:
```bash
git checkout -b feat/notificacao_discord
```

---

## 📤 Subindo Alterações
1. Faça as alterações no código.
2. Adicione os arquivos modificados à branch criada anteriormente:
   ```bash
   git add <nome_arquivo_modificado>
   ```
3. Faça o commit seguindo boas práticas:
   ```bash
   git commit -m "<categoria>: <descrição das alterações>"
   ```
   Exemplo:
   ```bash
   git commit -m "feat: Adiciona melhorias no loop de upload de arquivos no Google Drive"
   ```
4. Envie a branch para o repositório remoto:
   ```bash
   git push origin <NomeSuaBranch>
   ```
5. Crie um **Pull Request (PR)** no GitHub e solicite a revisão do código para uma par.
6. Após a aprovação, faça o merge da sua branch com a branch principal (`master`):
   ```bash
   git checkout master
   git pull origin master
   git merge <NomeSuaBranch>
   git push origin master
   ```

---

## ✅ Boas Práticas para Commits
- **Seja descritivo:** Explique claramente a mudança realizada.
- **Use o português de forma padronizada:** Mantenha a consistência.
- **Commits atômicos:** Faça commits pequenos e objetivos.

Exemplo de um commit bem estruturado:
```bash
git commit -m "fix: Corrige erro na extração de dados do API do Google Drive"
