# Brand assets - Integra Moda

Fonte e geradores da marca. Nada aqui é servido ao navegador: os arquivos publicados
são gerados a partir daqui e gravados em `assets/` e na raiz do site.

## Marca

| Item | Valor |
|---|---|
| Laranja da marca | `#FF5C01` |
| Tipografia do lockup | Inter Bold (SIL OFL 1.1, `fonts/Inter.ttf`) |
| Raio do ícone | 22% do lado |
| Tratamento do lockup | Uma linha só: "Integra" na cor do texto, **"Moda" em laranja**, centralizado na altura do símbolo |
| Proporção símbolo x nome | `MARK_SCALE = 0.78` no `gen_svg.py` - símbolo em 1,32x a altura da banda do nome |
| Respiro do símbolo dentro do ícone | 72% do lado (56% na versão maskable, 68% no apple-touch) |

O laranja da marca (`#FF5C01`) é diferente do laranja de interface do site (`#F97316`,
token `accent` do design system). O primeiro vale para o símbolo e os ícones; o segundo
segue valendo para CTA, bullets e labels.

## Arquivos fonte

| Arquivo | O que é |
|---|---|
| `mark-source-alpha.png` | Alfa do símbolo original recebido, 2048x2048, sem engrossamento. Fonte de tudo |
| `mark-trace.svg` | Traço vetorial do símbolo, gerado pelo `gen_trace.py`. Fonte dos SVG e dos ícones |
| `gen_trace.py` | Engrossa o alfa original e revetoriza com potrace: `python3 assets/brand/gen_trace.py 5` |
| `fonts/Inter.ttf` | Inter variável, usada para converter o texto do lockup em curvas |
| `fonts/OFL-Inter.txt` | Licença da Inter |
| `gen_svg.py` | Gera os lockups SVG (símbolo + "Integra Moda") com o texto em curvas |
| `gen_icons.py` | Gera ícone, símbolo, favicons, ícones de app, base64 - e chama o `gen_svg.py` antes |
| `base64/` | Data URIs prontos para e-mail, proposta e uso embutido |

## Regerar tudo

```bash
python3 assets/brand/gen_icons.py
```

Dependências: `rsvg-convert` (`brew install librsvg`), `magick` (`brew install imagemagick`),
`potrace` (`brew install potrace`, só para o `gen_trace.py`) e os pacotes Python
`uharfbuzz` e `fonttools`.

Para mudar a espessura do traço do símbolo, rode antes:

```bash
python3 assets/brand/gen_trace.py 5   # raio da dilatação, em px sobre o alfa de 2048
python3 assets/brand/gen_icons.py
```

O raio vigente é **5** (traço cerca de 15% mais grosso que o original recebido). Já foi 10 e
ficou pesado demais em uso pequeno. Acima de 13 o vão entre a diagonal e o laço central
fecha e o símbolo vira um bloco sólido. A espessura do **texto** não muda com isso - é a
Inter Bold, e ela ficou como estava.

## Saída

Em `assets/`: `icon.svg`, `logo-simbolo.svg/.png`, `logo-simbolo-invertido.svg/.png`,
`logo-horizontal.svg/.png`, `logo-horizontal-dark.svg/.png`, `safari-pinned-tab.svg`.

Em `assets/favicon/`: `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`,
`android-chrome-192x192.png`, `android-chrome-512x512.png`,
`android-chrome-maskable-512x512.png`, `mstile-150x150.png`.

Na raiz, só o que o navegador ou o sistema operacional procura em caminho fixo:
`favicon.ico`, `apple-touch-icon.png`, `site.webmanifest`, `browserconfig.xml`.

### Por que uns ficam na raiz e outros não

Regras completas de onde cada arquivo mora: seção **Asset Placement Rules** do `CLAUDE.md` na raiz do repositório.

| Arquivo | Motivo |
|---|---|
| `favicon.ico` | O navegador pede `/favicon.ico` sem ler o HTML - feed, página de erro, aba antes do HTML carregar |
| `apple-touch-icon.png` | O iOS sonda `/apple-touch-icon.png` na raiz quando não encontra o `<link>`. É rede de segurança |
| `browserconfig.xml` | Edge e IE legado pedem `/browserconfig.xml` na raiz por padrão |
| `site.webmanifest` | Precisa ser mesma origem; fica na raiz por convenção |
| `og-image.png` | Fica na raiz porque a URL já circula em links compartilhados - mover quebraria a prévia em re-scrape |

Todo o resto é referenciado por caminho declarado - no `<head>`, no manifest ou no
browserconfig - e por isso mora em `assets/favicon/`. Se mudar de lugar, mude nos três.

## Uso

- Fundo claro: `logo-horizontal.svg`. Fundo escuro: `logo-horizontal-dark.svg`.
- Contexto pequeno (≤32px) ou avatar: `icon.svg` ou `logo-simbolo-invertido.svg`.
- O texto do lockup já está em curvas - não depende da Inter instalada em lugar nenhum.
- O lockup tem **uma linha só**. A assinatura `PLM · ERP` saiu da arte em 11/09/2026 - quando ela for necessária, entra como texto ao lado da marca, não dentro dela.
