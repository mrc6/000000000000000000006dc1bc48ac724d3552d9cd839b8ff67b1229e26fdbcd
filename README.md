# 00000000000000000001556d6ebeeadb507bfaea032fc9edf879892a22fb94ac

# Jogo de Plataforma    
Este é um jogo de plataforma simples criado com a biblioteca pgzero. O jogo apresenta um herói que pode pular e se mover horizontalmente, inimigos como abelhas, lesmas de fogo e cracas, e obstáculos.

# Características do Jogo    
    
# Mecânica de Plataforma: O herói se move e salta em plataformas com física básica de gravidade.    
Construção de Nível: O mapa é construído a partir de arquivos CSV (platform_map.csv, obstacle_map.csv, char_map.csv, enemy_map.csv) que definem a posição das plataformas, obstáculos, do personagem e dos inimigos.    
Inimigos: O jogo inclui inimigos como abelhas (bee), lesmas de fogo (red_head) e cracas (tree), cada um com suas próprias animações e comportamentos.
Obstáculos: Existem obstáculos que, ao serem colididos, fazem o herói retornar à posição inicial.    
Objetivo: O herói precisa alcançar uma bandeira (goal_flag) para completar o nível, o que também o leva de volta ao início.    
    
# Como Jogar    
Certifique-se de ter o Python instalado.    
pip install -r requirements.txt    
Execute o arquivo run.py para iniciar o jogo (python run.py).    
Use as teclas de seta (left e right) para mover o herói horizontalmente.    
Use a barra de espaço para pular.    
Evite os inimigos e obstáculos para não voltar para o começo.    
    
# Estrutura do Repositório    
run.py: O código-fonte principal do jogo.            
platform_map.csv: Arquivo CSV que define a posição das plataformas.        
obstacle_map.csv: Arquivo CSV que define a posição dos obstáculos.    
char_map.csv: Arquivo CSV que define a posição inicial do personagem.    
enemy_map.csv: Arquivo CSV que define a posição dos inimigos.    
sounds: Pasta onde ficam guardados os sons utilizados no jogo.    
images: Paste onde ficam guardadas as imagens dos sprites do jogo.    
