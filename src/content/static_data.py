# report_data.py
# Este arquivo armazena todos os dados brutos (hardcoded)
# para manter o script principal limpo.

    ########################################################################
    ########################################################################
    #########################-------DADOS-------############################
    ########################################################################
    ########################################################################


dados_tabela_atos = [
    # Cabeçalho
    ("Ato Normativo", "Estrutura"),
    ("Lei Complementar nº 59/2001", "Contém a organização e a divisão judiciárias do Estado de Minas Gerais."),
    ("Resolução do Tribunal Pleno nº 03/2012", "Contém o Regimento Interno do Tribunal de Justiça."),
    ("Resolução nº 557/2008", "Dispõe sobre a criação da Comissão Estadual Judiciária de Adoção, CEJA-MG."),
    ("Resolução nº 640/2010", "Cria a Coordenadoria da Infância e da Juventude."),
    ("Resolução nº 673/2011", "Cria a Coordenadoria da Mulher em Situação de Violência Doméstica e Familiar."),
    ("Resolução nº 877/2018", "Instala, \"ad referendum\" do Órgão Especial, a 19ª Câmara Cível no Tribunal de Justiça."),
    ("Resolução nº 886/2019", "Determina a instalação da 8ª Câmara Criminal no Tribunal de Justiça."),
    ("Resolução nº 893/2019", "Determina a instalação da 20ª Câmara Cível no Tribunal de Justiça."),
    ("Resolução nº 1066/2023", "Dispõe sobre a estrutura e o funcionamento do Grupo de Monitoramento e Fiscalização do Sistema Carcerário e Socioeducativo - GMF no âmbito do Tribunal de Justiça do Estado de Minas Gerais."),
    ("Resolução nº 1080/2024", "Institui o Regulamento da Escola Judicial Desembargador Edésio Fernandes - EJEF."),
    ("Resolução nº 1086/2024", "Altera a Resolução do Órgão Especial nº 1.010, de 29 de agosto de 2020, que \"Dispõe sobre a implementação, a estrutura e o funcionamento dos \"Núcleos de Justiça 4.0\" e dá outras providências\", e altera a Resolução do Órgão Especial nº 1.053, de 20 de setembro de 2023, que \"Dispõe sobre a Superintendência Judiciária e dá outras providências\"."),
    ("Resolução nº 1125/2025", "Dispõe sobre os níveis hierárquicos das unidades organizacionais que integram a Secretaria do Tribunal de Justiça do Estado de Minas Gerais e define suas atribuições gerais."),
    ("Resolução nº 1128/2026", "Dispõe sobre a estrutura e o funcionamento das unidades organizacionais da Secretaria do Tribunal de Justiça diretamente vinculadas ou subordinadas à Presidência e dá outras providências.\n"
     "ü Secretaria de Governança e Gestão Estratégica - SEGOVE;\n"
     "ü Gabinete da Presidência - GAPRE;\n"
     "ü Assessoria Jurídica da Presidência - ASPRE;\n"
     "ü Diretoria Executiva de Comunicação - DIRCOM;\n"
     "ü Gabinete de Segurança Institucional - GSI;\n"
     "ü Diretoria Executiva de Planejamento Orçamentário e Qualidade na Gestão Institucional – DEPLAG;\n"
     "ü Gerência de Suporte aos Juizados Especiais - GEJESP;\n"
     "ü Assessoria de Precatórios - ASPREC;\n"
     "ü Secretaria de Auditoria Interna - SECAUD;\n"
     "- XI - Memória do Judiciário - MEJUD."),
    ("Resolução nº 1129/2026", "Dispõe sobre os Comitês e os Núcleos de Assessoramento à Presidência do Tribunal de Justiça do Estado de Minas Gerais - TJMG e dá outras providências.\n"
     "ü Comitê de Governança e Gestão Estratégica;\n"
     "ü Comitê Executivo de Gestão Institucional;\n"
     "ü Comitê Institucional de Inteligência;\n"
     "ü Comitê de Monitoramento e Suporte à Prestação Jurisdicional;\n"
     "ü Comitê de Governança de Tecnologia da Informação e Comunicação;\n"
     "ü Comitê Gestor de Segurança da Informação e Proteção de Dados Pessoais;\n"
     "ü Comitê Gestor da Política Judiciária para a Primeira Infância;\n"
     "ü Comitê Gestor Regional de Primeira Instância;\n"
     "ü Comitê Gestor de Atenção Integral à Saúde de Magistrados e Servidores;\n"
     "ü Comitê Orçamentário da Justiça de Segunda Instância;\n"
     "ü Comitê Orçamentário da Justiça de Primeira Instância;\n"
     "ü Núcleo de Cooperação Judiciária;\n"
     "ü Núcleo de Demandas Estruturais."),
    ("Resolução nº 1130/2026", "Dispõe sobre a Superintendência Administrativa e dá outras providências.\n"
     "ü Diretoria Executiva de Contratações - DIRCONT;\n"
     "ü Diretoria Executiva de Engenharia e Gestão Predial - DENGEP;\n"
     "ü Diretoria Executiva de Tecnologia da Informação e Comunicação - DIRTEC;\n"
     "ü Diretoria Executiva de Finanças e Execução Orçamentária - DIRFIN;\n"
     "ü Diretoria Executiva de Administração de Recursos Humanos - DEARHU."),
    ("Resolução nº 1136/2026", "Dispõe sobre a estrutura organizacional e o funcionamento da Superintendência Judiciária."),
    ("Resolução nº 1137/2026", "Dispõe sobre a estrutura organizacional e o funcionamento das Diretorias Executivas que compõem a Escola Judicial Desembargador Edésio Fernandes - EJEF."),
    ("Resolução nº 1138/2026", "Dispõe sobre a estrutura organizacional e o funcionamento da Superintendência de Tratamento Adequado dos Conflitos de Interesses."),
    ("Resolução nº 1139/2026", "Dispõe sobre a reestruturação da Corregedoria Geral de Justiça."),
    ("Resolução nº 1140/2026", "Dispõe sobre a estrutura, as atribuições e o funcionamento da Ouvidoria do Tribunal de Justiça do Estado de Minas Gerais.")
]

dados_tabela_areas = [
    # Tipo, Coluna 1 (Denominação), Coluna 2 (Sigla)
    # Cabeçalho Principal
    ("HEADER_MAIN", "DENOMINAÇÃO", ""),    # Comitês e Núcleos (Sem Sigla na entrada fornecida)
    ("DATA_MERGED", "Comitê de Governança de Tecnologia da Informação e Comunicação", ""),
    ("DATA_MERGED", "Comitê de Governança e Gestão Estratégica", ""),
    ("DATA_MERGED", "Comitê de Monitoramento e Suporte à Prestação Jurisdicional", ""),
    ("DATA_MERGED", "Comitê Executivo de Gestão Institucional", ""),
    ("DATA_MERGED", "Comitê Gestor da Política Judiciária para a Primeira Infância", ""),
    ("DATA_MERGED", "Comitê Gestor de Atenção Integral à Saúde de Magistrados e Servidores", ""),
    ("DATA_MERGED", "Comitê Gestor de Segurança da Informação e Proteção de Dados Pessoais", ""),
    ("DATA_MERGED", "Comitê Gestor Regional de Primeira Instância", ""),
    ("DATA_MERGED", "Comitê Institucional de Inteligência", ""),
    ("DATA_MERGED", "Comitê Orçamentário da Justiça de Primeira Instância", ""),
    ("DATA_MERGED", "Comitê Orçamentário da Justiça de Segunda Instância", ""),
    ("DATA_MERGED", "Núcleo de Cooperação Judiciária", ""),
    ("DATA_MERGED", "Núcleo de Demandas Estruturais", ""),    # Unidades da Presidência
    ("HEADER_GROUP_SIGLA", "UNIDADES ORGANIZACIONAIS DIRETAMENTE VINCULADAS OU SUBORDINADAS À PRESIDÊNCIA", "SIGLA"),
    ("DATA_SPLIT", "Assessoria de Precatórios", "ASPREC"),
    ("DATA_SPLIT", "Assessoria Jurídica da Presidência", "ASPRE"),
    ("DATA_SPLIT", "Diretoria Executiva de Comunicação", "DIRCOM"),
    ("DATA_SPLIT", "Diretoria Executiva de Planejamento Orçamentário e Qualidade na Gestão Institucional", "DEPLAG"),
    ("DATA_SPLIT", "Gabinete da Presidência", "GAPRE"),
    ("DATA_SPLIT", "Gabinete de Segurança Institucional", "GSI"),
    ("DATA_SPLIT", "Gerência de Suporte aos Juizados Especiais", "GEJESP"),
    ("DATA_SPLIT", "Memória do Judiciário", "MEJUD"),
    ("DATA_SPLIT", "Secretaria de Auditoria Interna", "SECAUD"),
    ("DATA_SPLIT", "Secretaria de Governança e Gestão Estratégica", "SEGOVE"),    # Superintendência Administrativa
    ("HEADER_GROUP_SIGLA", "SUPERINTENDÊNCIA ADMINISTRATIVA", "SIGLA"),
    ("DATA_SPLIT", "Diretoria Executiva de Administração de Recursos Humanos", "DEARHU"),
    ("DATA_SPLIT", "Diretoria Executiva de Contratações", "DIRCONT"),
    ("DATA_SPLIT", "Diretoria Executiva de Engenharia e Gestão Predial", "DENGEP"),
    ("DATA_SPLIT", "Diretoria Executiva de Tecnologia da Informação e Comunicação", "DIRTEC"),    # 1ª Vice-Presidência
    ("HEADER_GROUP_SIGLA", "SUPERINTENDÊNCIA JUDICIÁRIA", "SIGLA"),
    ("DATA_SPLIT", "Assessoria da 1ª Vice-Presidência", "1ª ASVIP"),
    ("DATA_SPLIT", "Diretoria Executiva de Suporte à Prestação Jurisdicional", "DIRSUP"),
    ("DATA_SPLIT", "Gabinete da 1ª Vice-Presidência", "1º GAVIP"),
    ("DATA_SPLIT", "Gabinetes dos Desembargadores", "GADES"),
    ("DATA_SPLIT", "Gerências dos Cartórios das Câmaras", "GECART"),
    ("DATA_SPLIT", "Secretaria de Padronização e Acompanhamento da Gestão Judiciária", "SEPAD"),    # 2ª Vice-Presidência
    ("HEADER_GROUP_SIGLA", "SUPERINTENDÊNCIA DA ESCOLA JUDICIAL DESEMBARGADOR EDÉSIO FERNANDES – EJEF", "SIGLA"),
    ("DATA_SPLIT", "Diretoria Executiva de Desenvolvimento de Pessoas", "DIRDEP"),
    ("DATA_SPLIT", "Diretoria Executiva de Gestão da Informação Documental", "DIRGED"),    # 3ª Vice-Presidência
    ("HEADER_GROUP_SIGLA", "SUPERINTENDÊNCIA DA SUPERINTENDÊNCIA DE TRATAMENTO ADEQUADO DOS CONFLITOS DE INTERESSE", "SIGLA"),
    ("DATA_SPLIT", "Assessoria da 3ª Vice-Presidência", "3ª ASVIP"),
    ("DATA_SPLIT", "Comitê de Justiça Restaurativa", "COMJUR"),
    ("DATA_SPLIT", "Diretoria Executiva de Planejamento e Gestão da 3ª Vice-Presidência", "DIRTEVI"),
    ("DATA_SPLIT", "Gabinete da 3ª Vice-Presidência", "3º GAVIP"),
    ("DATA_SPLIT", "Núcleo Permanente de Métodos Consensuais de Solução de Conflitos", "NUPEMEC"),    # Corregedoria
    ("HEADER_GROUP_SIGLA", "SUPERINTENDÊNCIA DA SECRETARIA DA CORREGEDORIA-GERAL DE JUSTIÇA E DOS SERVIÇOS JUDICIAIS, NOTARIAIS E DE REGISTRO DO ESTADO", "SIGLA"),
    ("DATA_SPLIT", "Diretoria Executiva da Atividade Correcional", "DIRCOR"),
    ("DATA_SPLIT", "Diretoria Executiva dos Serviços Notariais e de Registro", "DIRNOT"),
    ("DATA_SPLIT", "Secretaria de Suporte ao Planejamento e à Gestão da Primeira Instância", "SEPLAN")
]

dados_tabela_estrutura = [
    # Tipo, Coluna 1
    ("HEADER_MAIN", "ESTRUTURAS PARA A PRESTAÇÃO JURISDICIONAL NA SEGUNDA INSTÂNCIA"),
    
    # Câmaras Cíveis
    ("HEADER_GROUP_MERGED", "Câmaras Cíveis"),
    ("DATA_MERGED", "01ª Câmara Cível"),
    ("DATA_MERGED", "02ª Câmara Cível"),
    ("DATA_MERGED", "03ª Câmara Cível"),
    ("DATA_MERGED", "04ª Câmara Cível Especializada"),
    ("DATA_MERGED", "05ª Câmara Cível"),
    ("DATA_MERGED", "06ª Câmara Cível"),
    ("DATA_MERGED", "07ª Câmara Cível"),
    ("DATA_MERGED", "08ª Câmara Cível Especializada"),
    ("DATA_MERGED", "09ª Câmara Cível"),
    ("DATA_MERGED", "10ª Câmara Cível"),
    ("DATA_MERGED", "11ª Câmara Cível"),
    ("DATA_MERGED", "12ª Câmara Cível"),
    ("DATA_MERGED", "13ª Câmara Cível"),
    ("DATA_MERGED", "14ª Câmara Cível"),
    ("DATA_MERGED", "15ª Câmara Cível"),
    ("DATA_MERGED", "16ª Câmara Cível Especializada"),
    ("DATA_MERGED", "17ª Câmara Cível"),
    ("DATA_MERGED", "18ª Câmara Cível"),
    ("DATA_MERGED", "19ª Câmara Cível"),
    ("DATA_MERGED", "20ª Câmara Cível"),
    ("DATA_MERGED", "21ª Câmara Cível Especializada"),

    # Câmaras Criminais
    ("HEADER_GROUP_MERGED", "Câmaras Criminais"),
    ("DATA_MERGED", "01ª Câmara Criminal"),
    ("DATA_MERGED", "02ª Câmara Criminal"),
    ("DATA_MERGED", "03ª Câmara Criminal"),
    ("DATA_MERGED", "04ª Câmara Criminal"),
    ("DATA_MERGED", "05ª Câmara Criminal"),
    ("DATA_MERGED", "06ª Câmara Criminal"),
    ("DATA_MERGED", "07ª Câmara Criminal"),
    ("DATA_MERGED", "08ª Câmara Criminal"),
    ("DATA_MERGED", "09ª Câmara Criminal Especializada"),

    # Justiça 4.0 - Cível
    ("HEADER_GROUP_MERGED", "Justiça 4.0 - Cível"),
    ("DATA_MERGED", "1º Núcleo de Justiça 4.0 - Cível Família (1º NUCIF 4.0)"),
    ("DATA_MERGED", "2º Núcleo de Justiça 4.0 - Cível Família (2º NUCIF 4.0)"),
    ("DATA_MERGED", "3º Núcleo de Justiça 4.0 - Cível Família (3º NUCIF 4.0)"),
    ("DATA_MERGED", "4º Núcleo de Justiça 4.0 - Cível Família (4º NUCIF 4.0)"),
    ("DATA_MERGED", "1º Núcleo de Justiça 4.0 - Cível Privado (1º NUCIP 4.0)"),
    ("DATA_MERGED", "2º Núcleo de Justiça 4.0 - Cível Privado (2º NUCIP 4.0)"),
    ("DATA_MERGED", "3º Núcleo de Justiça 4.0 - Cível Privado (3º NUCIP 4.0)"),
    ("DATA_MERGED", "4º Núcleo de Justiça 4.0 - Cível Privado - (4º NUCIP 4.0)"),
    ("DATA_MERGED", "5º Núcleo de Justiça 4.0 - Cível Privado - (5º NUCIP 4.0)"),
    ("DATA_MERGED", "6º Núcleo de Justiça 4.0 - Cível Privado - (6º NUCIP 4.0)"),
    
    # Justiça 4.0 - Criminal
    ("HEADER_GROUP_MERGED", "Justiça 4.0 - Criminal"),
    ("DATA_MERGED", "1º Núcleo de Justiça 4.0 - Criminal Especializado (1º NUCRES 4.0)"),
    ("DATA_MERGED", "2º Núcleo de Justiça 4.0 - Criminal Especializado (2º NUCRES 4.0)"),
    ("DATA_MERGED", "3º Núcleo de Justiça 4.0 - Criminal Especializado (3º NUCRES 4.0)")
]

dados_tabela_comarcas = [
    # Tipo, Col 1, Col 2, Col 3, Col 4
    ("HEADER_MERGE_4", "COMARCAS INSTALADAS", "", "", ""),
    ("DATA_4_COL", "Abaeté", "Abre Campo", "Açucena", "Águas Formosas"),
    ("DATA_4_COL", "Aimorés", "Aiuruoca", "Além Paraíba", "Alvinópolis"),
    ("DATA_4_COL", "Andradas", "Andrelândia", "Alfenas", "Almenara"),
    ("DATA_4_COL", "Areado", "Arinos", "Alpinópolis", "Alto Rio Doce"),
    ("DATA_4_COL", "Araçuaí", "Araguari", "Araxá", "Arcos"),
    ("DATA_4_COL", "Baependi", "Bambuí", "Barão de Cocais", "Barbacena"),
    ("DATA_4_COL", "Barroso", "Belo Horizonte", "Belo Vale", "Betim"),
    ("DATA_4_COL", "Bicas", "Boa Esperança", "Bocaiúva", "Bom Despacho"),
    ("DATA_4_COL", "Bom Sucesso", "Bonfim", "Bonfinópolis de Minas", "Borda da Mata"),
    ("DATA_4_COL", "Botelhos", "Brasília de Minas", "Brazópolis", "Brumadinho"),
    ("DATA_4_COL", "Bueno Brandão", "Buenópolis", "Buritis", "Cabo Verde"),
    ("DATA_4_COL", "Cachoeira de Minas", "Caeté", "Caldas", "Camanducaia"),
    ("DATA_4_COL", "Cambuí", "Cambuquira", "Campanha", "Campestre"),
    ("DATA_4_COL", "Campina Verde", "Campo Belo", "Campos Altos", "Campos Gerais"),
    ("DATA_4_COL", "Canápolis", "Candeias", "Capelinha", "Capinópolis"),
    ("DATA_4_COL", "Carandaí", "Carangola", "Caratinga", "Carlos Chagas"),
    ("DATA_4_COL", "Carmo da Mata", "Carmo de Minas", "Carmo do Cajuru", "Carmo do Paranaíba"),
    ("DATA_4_COL", "Carmo do Rio Claro", "Carmópolis de Minas", "Cássia", "Cataguases"),
    ("DATA_4_COL", "Caxambu", "Cláudio", "Conceição das Alagoas", "Conceição do Mato Dentro"),
    ("DATA_4_COL", "Conceição do Rio Verde", "Congonhas", "Conquista", "Conselheiro Lafaiete"),
    ("DATA_4_COL", "Conselheiro Pena", "Contagem", "Coração de Jesus", "Corinto"),
    ("DATA_4_COL", "Coromandel", "Coronel Fabriciano", "Cristina", "Cruzília"),
    ("DATA_4_COL", "Curvelo", "Diamantina ", "Divino", "Divinópolis"),
    ("DATA_4_COL", "Dores do Indaiá", "Elói Mendes", "Entre-Rios de Minas", "Ervália"),
    ("DATA_4_COL", "Esmeraldas", "Espera Feliz", "Espinosa", "Estrela do Sul"),
    ("DATA_4_COL", "Eugenópolis", "Extrema", "Ferros", "Formiga"),
    ("DATA_4_COL", "Francisco Sá", "Frutal", "Galiléia", "Governador Valadares"),
    ("DATA_4_COL", "Grão-Mogol", "Guanhães", "Guapé", "Guaranésia"),
    ("DATA_4_COL", "Guarani", "Guaxupé", "Ibiá", "Ibiraci"),
    ("DATA_4_COL", "Ibirité", "Igarapé", "Iguatama", "Inhapim"),
    ("DATA_4_COL", "Ipanema", "Ipatinga", "Itabira", "Itabirito"),
    ("DATA_4_COL", "Itaguara", "Itajubá", "Itamarandiba", "Itambacuri"),
    ("DATA_4_COL", "Itamogi", "Itamonte", "Itanhandu", "Itanhomi"),
    ("DATA_4_COL", "Itapagipe", "Itapecerica", "Itaúna", "Ituiutaba"),
    ("DATA_4_COL", "Itumirim", "Iturama", "Jaboticatubas", "Jacinto"),
    ("DATA_4_COL", "Jacuí", "Jacutinga", "Jaíba", "Janaúba"),
    ("DATA_4_COL", "Januária", "Jequeri", "Jequitinhonha", "João Monlevade"),
    ("DATA_4_COL", "João Pinheiro", "Juatuba", "Juíz de Fora", "Lagoa da Prata"),
    ("DATA_4_COL", "Lagoa Santa", "Lajinha", "Lambari", "Lavras"),
    ("DATA_4_COL", "Leopoldina", "Lima Duarte", "Luz", "Machado"),
    ("DATA_4_COL", "Malacacheta", "Manga", "Manhuaçu", "Manhumirim"),
    ("DATA_4_COL", "Mantena", "Mar de Espanha", "Mariana", "Martinho Campos"),
    ("DATA_4_COL", "Mateus Leme", "Matias Barbosa", "Matozinhos", "Medina"),
    ("DATA_4_COL", "Mercês", "Mesquita", "Minas Novas", "Miradouro"),
    ("DATA_4_COL", "Miraí", "Montalvânia", "Monte Alegre de Minas", "Monte Azul"),
    ("DATA_4_COL", "Monte Belo", "Monte Carmelo", "Monte Santo de Minas", "Monte Sião"),
    ("DATA_4_COL", "Montes Claros", "Morada Nova de Minas", "Muriaé", "Mutum"),
    ("DATA_4_COL", "Muzambinho", "Nanuque", "Natércia", "Nepomuceno"),
    ("DATA_4_COL", "Nova Era", "Nova Lima", "Nova Ponte", "Nova Resende"),
    ("DATA_4_COL", "Nova Serrana", "Novo Cruzeiro", "Oliveira", "Ouro Branco"),
    ("DATA_4_COL", "Ouro Fino", "Ouro Preto", "Palma", "Pará de Minas"),
    ("DATA_4_COL", "Paracatu", "Paraguaçu", "Paraisópolis", "Paraopeba "),
    ("DATA_4_COL", "Passa Quatro", "Passa Tempo", "Passos", "Patos de Minas"),
    ("DATA_4_COL", "Patrocínio", "Peçanha", "Pedra Azul", "Pedralva"),
    ("DATA_4_COL", "Pedro Leopoldo", "Perdizes", "Perdões", "Piranga"),
    ("DATA_4_COL", "Pirapetinga", "Pirapora", "Pitangui", "Piumhi"),
    ("DATA_4_COL", "Poço Fundo", "Poços de Caldas", "Pompéu", "Ponte Nova"),
    ("DATA_4_COL", "Porteirinha", "Pouso Alegre", "Prados", "Prata"),
    ("DATA_4_COL", "Pratápolis", "Presidente Olegário", "Raul Soares", "Resende Costa"),
    ("DATA_4_COL", "Resplendor", "Ribeirão das Neves", "Rio Casca", "Rio Novo"),
    ("DATA_4_COL", "Rio Paranaíba", "Rio Pardo de Minas", "Rio Piracicaba", "Rio Pomba"),
    ("DATA_4_COL", "Rio Preto", "Rio Vermelho", "Sabará", "Sabinópolis"),
    ("DATA_4_COL", "Sacramento", "Salinas", "Santa Bárbara", "Santa Luzia"),
    ("DATA_4_COL", "Santa Maria do Suaçuí", "Santa Rita de Caldas", "Santa Rita do Sapucaí", "Santa Vitória"),
    ("DATA_4_COL", "Santo Antônio do Monte", "Santos Dumont", "São Domingos do Prata", "São Francisco"),
    ("DATA_4_COL", "São Gonçalo do Sapucaí", "São Gotardo", "São João da Ponte", "São João Del Rei"),
    ("DATA_4_COL", "São João do Paraíso", "São João Evangelista", "São João Nepomuceno", "São Lourenço"),
    ("DATA_4_COL", "São Romão", "São Roque de Minas", "São Sebastião do Paraíso", "Senador Firmino"),
    ("DATA_4_COL", "Serro", "Sete Lagoas", "Silvianópolis", "Taiobeiras"),
    ("DATA_4_COL", "Tarumirim", "Teixeiras", "Teófilo Otoni", "Timóteo"),
    ("DATA_4_COL", "Tiros", "Tombos", "Três Corações", "Três Marias"),
    ("DATA_4_COL", "Três pontas", "Tupaciguara", "Turmalina", "Ubá"),
    ("DATA_4_COL", "Uberaba", "Uberlândia", "Unaí", "Varginha"),
    ("DATA_4_COL", "Várzea da Palma", "Vazante", "Vespasiano", "Viçosa"),
    ("DATA_4_COL", "Virginópolis", "Visconde do Rio Branco", "", ""),
]

dados_tabela_nucleos = [
    # Tipo, Col 1
    ("HEADER_GROUP_MERGED", "Núcleos de Justiça 4.0 – 1ª Instância"), 
    ("DATA_MERGED", "Núcleo de Justiça 4.0 - Cooperação Judiciária (Foco em Brumadinho e, agora, previdenciário)"),
    ("DATA_MERGED", "Núcleo de Justiça 4.0 – Cível"),
    ("DATA_MERGED", "Núcleo de Justiça 4.0 – Criminal"),
    ("DATA_MERGED", "Núcleo de Justiça 4.0 - Fazenda Pública"),
    ("DATA_MERGED", "Núcleo de Justiça 4.0 – Juizado Especial")
]

dados_tabela_processos = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5, Col 6, Col 7
        # Gerado automaticamente a partir da planilha Informações TJMG_CEINFO.xlsx
        ('HEADER_MERGE', 'PROCESSOS DISTRIBUÍDOS', '', '', '', '', '', '', ''),
        ('SUB_HEADER', 'Instância', '2021.0', '2022.0', '2023.0', '2024.0', '2025.0', 'Média'),
        ('DATA_ROW', 'Justiça Comum', '1365924.0', '1565819.0', '1710153.0', '1675686.0', '1679349', '1531426'),
        ('DATA_ROW', 'Juizado Especial', '536797.0', '558504.0', '622683.0', '661356.0', '578088', '581967'),
        ('DATA_ROW', 'Turma Recursal', '84268.0', '84215.0', '93299.0', '103728.0', '106876', '88079'),
        ('DATA_ROW', '2º Grau', '222614.0', '227760.0', '271256.0', '334528.0', '368713', '270721'),
]

dados_tabela_julgamentos = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5, Col 6, Col 7
    ("HEADER_MERGE", "JULGAMENTOS", "", "", "", "", "", "", ""),
    ("SUB_HEADER", "Instância", "2021", "2022", "2023", "2024", "2025", "Média"),
    ("DATA_ROW", "Justiça Comum", "1015223", "1185589", "1320950", "1412397", "1480894", "1215626"),
    ("DATA_ROW", "Juizado Especial", "636208", "810834", "932469", "920189", "884599", "774097"),
    ("DATA_ROW", "Turma Recursal", "67797", "77926", "105764", "117904", "147371", "232577"),
    ("DATA_ROW", "2º Grau", "225454", "236418", "275286", "337993", "358728", "247770"),
    ("TOTAL_ROW", "Total", "1944682", "2310767", "2634469", "2788483", "2871592", "2470072")
]

dados_tabela_acervo = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5, Col 6, Col 7
    ("HEADER_MERGE", "ACERVO DE FEITOS ATIVOS NO ÚLTIMO DIA DO ANO", "", "", "", "", "", ""),
    ("SUB_HEADER", "Instância", "2021", "2022", "2023", "2024", "2025", "Média"),
    ("DATA_ROW", "Justiça Comum", "4152223", "4233968", "4140228", "4042435", "3967597", "4131935"),
    ("DATA_ROW", "Juizado Especial", "1125081", "1053185", "963386", "922153", "840190", "1004900"),
    ("DATA_ROW", "Turma Recursal", "67940", "69541", "76573", "87801", "79767", "70482"),
    ("DATA_ROW", "2º Grau", "232448", "224156", "220826", "206944", "235708", "224132"),
    ("TOTAL_ROW", "Total", "5577692", "5580850", "5401013", "5259333", "5123262", "5431450")
]

TITULO_TABELA_ORCAMENTO_1 = "Unidade Orçamentária 1031 – TJMG | Crédito Autorizado x Despesa Realizada por Ação Orçamentária – 2025"

dados_tabela_orcamento = [
    # A linha HEADER_MERGE foi removida daqui!
    ["SUB_HEADER", "AÇÃO ORÇAMENTÁRIA", "CRÉDITO AUTORIZADO 2025 (R$)", "DESPESA REALIZADA 2025 (R$)", "%"],
    ["DATA_ROW", "2053 - Remuneração de Magistrados da Ativa E Encargos Sociais", "1715985406", "1715985406", "100%"],
    ["DATA_ROW", "2054 - Remuneração de Servidores da Ativa e Encargos Sociais", "6275094319", "6275003585", "100%"],
    ["DATA_ROW", "7006 - Proventos de Inativos Civis e Pensionistas", "3119181127", "2954301230", "95%"],
    ["DATA_ROW", "7004 - Precatórios e Sentenças Judiciárias", "1000", "-", "0%"],
    ["TOTAL_ROW", "TOTAL", "11110261852", "10945290221", "99%"]
]

TITULO_TABELA_ORCAMENTO_2 = "Unidade Orçamentária 4031 – FEPJ | Crédito Autorizado x Despesa Realizada por Ação Orçamentária – 2025"

dados_tabela_orcamento_acao = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5, Col 6, Col 7
    ["SUB_HEADER", "AÇÃO ORÇAMENTÁRIA", "CRÉDITO AUTORIZADO 2025 (R$)", "DESPESA REALIZADA 2025 (R$)", "%"],
    ("DATA_ROW", "2053 - Remuneração de Magistrados da Ativa E Encargos Sociais", "1715985406", "1715985406", "100%"),
    ("DATA_ROW", "2054 - Remuneração de Servidores da Ativa e Encargos Sociais", "6275094319", "6275003585", "100%"),
    ("DATA_ROW", "7006 - Proventos de Inativos Civis e Pensionistas", "3119181127", "2954301230", "95%"),
    ("DATA_ROW", "7004 - Precatórios e Sentenças Judiciárias", "1000", "-", "0%"),
    ("TOTAL_ROW", "TOTAL", "11110261852", "10945290221", "99%")
]

TITULO_TABELA_ORCAMENTO_ACAO = "Unidades Orçamentárias 1031 – TJMG e 4031 – FEPJ Orçamento 2026 por Ação"

dados_tabela_orcamento_2025 = [ 
    # Título do Grupo 1 (UO 1031)
    ("GROUP_TITLE", "UO 1031 – TJMG", ""), 
    ("SUB_HEADER", "Ação Orçamentária", "Valor (R$)"),
    ("DATA_ROW", "7004 - Precatórios e Sentenças Judiciais", "1000"),
    ("DATA_ROW", "7006 - Proventos de Inativos Civis e Pensionistas", "3387367697"),
    ("DATA_ROW", "2053 - Remuneração de Magistrados da Ativa", "1911006918"),
    ("DATA_ROW", "2054 - Remuneração de Servidores da Ativa", "7198503821"),
    ("TOTAL_ROW", "VALOR TOTAL – UO 1031", "12496879436"), # Fim do primeiro bloco
    
    # Título do Grupo 2 (UO 4031) - Começa na linha seguinte
    ("GROUP_TITLE", "UO 4031 – FEPJ", ""), 
    ("SUB_HEADER", "Ação Orçamentária", "Valor (R$)"),
    ("DATA_ROW", "2025 - Gestão de Serviços De TIC", "364742031"),
    ("DATA_ROW", "2055 - Auxílios Concedidos a Magistrados", "270000000"),
    ("DATA_ROW", "2091 - Obras e Gestão Predial", "712057538"),
    ("DATA_ROW", "2109 - Formação, Aperfeiçoamento e Desenvolvimento Contínuo De Pessoas", "6250000"),
    ("DATA_ROW", "4395 - Processamento Judiciário", "2374248423"),
    ("TOTAL_ROW", "VALOR TOTAL – UO 4031", "3727297992"),
]

TITULO_TABELA_ORCAMENTO_ACAO_COMPARACAO = "Unidades Orçamentárias 1031 – TJMG e 4031 – FEPJ Comparativo Orçamento 2025 x 2026"

dados_tabela_orcamento_comparacao = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5
    ("GROUP_TITLE", "UO 1031 – TJMG", ""), 
    ("SUB_HEADER", "Ação Orçamentária", "2025", "%", "2026"),
    ("DATA_ROW", "7004 - Precatórios e Sentenças Judiciais", "1000", "0%", "1000"),
    ("DATA_ROW", "7006 - Proventos de Inativos Civis e Pensionistas", "3119181127", "9%", "3387367697"),
    ("DATA_ROW", "2053 - Remuneração de Magistrados da Ativa e Encargos Sociais", "1715985406", "11%", "1911006918"),
    ("DATA_ROW", "2054 - Remuneração de Servidores da Ativa e Encargos Sociais", "6275094319", "15%", "7198503821"),
    ("TOTAL_ROW", "VALOR TOTAL – UO 4031", "11110263877", "12,48%", "12496879436"),

    ("GROUP_TITLE", "UO 1031 – TJMG", ""), 
    ("SUB_HEADER", "Ação Orçamentária", "2025", "%", "2026"),
    ("DATA_ROW", "2025 - Gestão de Serviços De TIC", "265699614", "37%", "364742031"),
    ("DATA_ROW", "2055 - Auxílios Concedidos a Magistrados e Servidores", "220000000", "23%", "270000000"),
    ("DATA_ROW", "2091 - Obras e Gestão Predial", "650796141", "9%", "712057538"),
    ("DATA_ROW", "2109 - Formação, Aperfeiçoamento e Desenvolvimento Contínuo De Pessoas", "4900000", "28%", "6250000"),
    ("DATA_ROW", "4395 - Processamento Judiciário", "2714248423", "-4%", "2374248423"),
    ("TOTAL_ROW", "VALOR TOTAL – UO 4031", "3612835151", "3,17%", "3727297992"),
]

dados_tabela_cidades = [
    # Tipo, Col 1, Col 2, Col 3, Col 4
    ("DATA_ROW", "Brasília de Minas", "Caeté", "Frutal", "Itajubá"),
    ("DATA_ROW", "João Monlevade", "Manhuaçu", "Mariana", "Monte Carmelo"),
    ("DATA_ROW", "Montes Claros", "Muriaé", "Nova Serrana", "Ponte Nova"),
    ("DATA_ROW", "Porteirinha", "Uberaba", "Unaí", "Vazante"),
]

dados_tabela_justica_numeros = [
    # Tipo, Col 1, Col 2, Col 3, Col 4, Col 5, Col 6, Col 7
    ("HEADER_MERGE", "RELATÓRIO JUSTIÇA EM NÚMEROS (CNJ) | DADOS ANUAIS DO TJMG", "", "", "", "", "", ""),
    ("SUB_HEADER", "Ano de edição do relatório", "2019", "2020", "2021", "2022", "2023", "2024"),
    ("SUB_HEADER_SECONDARY", "Ano base", "2018", "2019", "2020", "2021", "2022", "2023"),
    
    # ---------------------------------------------------------------------------------------
    # DADOS ESTATÍSTICOS GERAIS
    # ---------------------------------------------------------------------------------------
    ("DATA_ROW", "Nº de municípios-sede", "296", "296", "297", "297", "298", "298"),
    ("DATA_ROW", "Percentual da população em munícipios-sede", "81,6%", "81,6%", "81,6%", "81,6%", "82%", "82%"),
    ("DATA_ROW", "Nº de unidades judiciárias (Estrutura de 1º grau)", "848", "861", "870", "778", "896", "962"),
    ("DATA_ROW", "Classificação do TJMG dentro do Grupo ‘Grande Porte’", "3º lugar", "3º lugar", "2º lugar", "3º lugar", "2º lugar", "2º lugar"),
    ("DATA_ROW", "Nº de magistrados", "1.030", "1.083", "1.085", "1.065", "1.044", "1.022"),
    ("DATA_ROW", "Força de trabalho (servidores e auxiliares) (*)", "27.847", "28.037", "27.334", "24.221", "32.887", "32.695"),
    ("DATA_ROW", "Despesa total da justiça (Bilhões)", "5.098.319.857", "5.790.909.062", "6.396.561.674", "6.735.890.808", "8.108.940.000", "9.634.461.461"),
    ("DATA_ROW", "Despesa total por habitante, incluindo custo com inativos (Reais)", "242,3", "273,6", "300,4", "314,6", "376,1", "469,1"),
    ("DATA_ROW", "Custo médio mensal com magistrados (Milhões)", "40.541", "63.158", "70.997", "78.596", "170.287", "84.349"),
    ("DATA_ROW", "Custo médio mensal com servidores (Milhões)", "14.462", "16.229", "17.810", "19.117", "45.416", "27.454"),
    ("DATA_ROW", "Percentual de cargos vagos de magistrados", "37,6%", "34,4%", "34,2%", "35,5%", "36,7%", "38,10%"),
    ("DATA_ROW", "Percentual de servidores lotados na área administrativa", "s/d", "9%", "10%", "10%", "10%", "9%"),
    ("DATA_ROW", "Casos novos", "1.717.862", "1.649.250", "1.428.480", "1.478.922", "1.724.611", "6.863.658"),
    ("DATA_ROW", "Casos pendentes", "3.942.814", "3.772.400", "3.940.277", "4.369.191", "4.271.123", "4.041.123"),
    ("DATA_ROW", "Casos novos por 100 mil habitantes", "7.187", "7.027", "6.133", "6.265", "7.303", "8.786"),
    ("DATA_ROW", "Índice de produtividade dos magistrados", "1.984", "2.019", "1.471", "1.500", "1.885", "1.400"),
    ("DATA_ROW", "Índice de produtividade de servidores da área judiciária", "150", "154", "118", "124", "152", "109"),
    ("DATA_ROW", "Percentual de servidores (as) na área judiciária de primeiro grau", "s/d", "88%", "88%", "88%", "88%", "87%"),
    ("DATA_ROW", "Índice de atendimento à demanda (Geral)", "110,6%", "116,5%", "103,6%", "101,8%", "106,9%", "91%"),
    ("DATA_ROW", "Percentual de casos novos eletrônicos", "39,5%", "64,5%", "83,7%", "84,2%", "96,5%", "98,40%"),
    ("DATA_ROW", "Percentual de unidades judiciárias de primeiro grau com Juízo 100% Digital", "s/d", "s/d", "12%", "47,8%", "99,1%", "92,20%"),
    ("DATA_ROW", "Quantidade de Núcleos de Justiça 4.0", "s/d", "s/d", "s/d", "2", "5", "9"),
    ("DATA_ROW", "Quantidade de Balcões Virtuais instalados", "s/d", "s/d", "s/d", "s/d", "1.421", "1.485"),
    ("DATA_ROW", "Casos novos por magistrados - 1º grau", "1.550", "1.556", "1.274", "1.308", "1.649", "1.848"),
    ("DATA_ROW", "Casos novos por magistrados - 2º grau", "1.760", "1.602", "1.448", "1.502", "1.388", "2.106"),
    ("DATA_ROW", "Casos novos por servidor da área judiciária – 1º grau", "115", "116", "100", "105", "129", "144"),
    ("DATA_ROW", "Casos novos por servidor da área judiciária – 2º grau", "152", "145", "136", "149", "135", "196"),
    ("DATA_ROW", "Carga de trabalho do magistrado – 1º grau", "6.637", "6.583", "3.867", "6.552", "7.040", "6.817"),
    ("DATA_ROW", "Carga de trabalho do magistrado – 2º grau", "4.360", "4.169", "3.891", "3.867", "3.099", "3.898"),
    ("DATA_ROW", "Carga de trabalho do servidor da área judiciária – 1º grau", "492", "490", "462", "527", "551", "531"),
    ("DATA_ROW", "Carga de trabalho do servidor da área judiciária – 2º grau", "376", "376", "364", "383", "300", "363"),
    ("DATA_ROW", "Índice de produtividade dos magistrados – 1º grau", "2.045", "2.079", "1.503", "1.498", "1.966", "1.936"),
    ("DATA_ROW", "Índice de produtividade dos magistrados – 2º grau", "1.590", "1.669", "1.271", "1.509", "1.421", "1.740"),
    ("DATA_ROW", "Índice de produtividade dos servidores da área judiciária – 1º grau", "151", "155", "117", "121", "154", "151"),
    ("DATA_ROW", "Índice de produtividade dos servidores da área judiciária – 2º grau", "137", "151", "119", "149", "138", "162"),
    ("DATA_ROW", "Índice de casos novos eletrônicos", "s/d", "s/d", "83,7%", "84,2%", "96,5%", "98,40%"),
    ("DATA_ROW", "Índice de casos novos eletrônicos – 1º grau", "42%", "66%", "85%", "85%", "97%", "98,00%"),
    ("DATA_ROW", "Índice de casos novos eletrônicos – 2º grau", "28%", "53%", "78%", "83%", "91%", "98,00%"),
    ("DATA_ROW", "Índice de atendimento à demanda – 1º grau", "114%", "118%", "106%", "102%", "107%", "87,00%"),
    ("DATA_ROW", "Índice de atendimento à demanda – 2º grau", "90%", "104%", "88%", "100%", "102%", "83,00%"),
    ("DATA_ROW", "Taxa de congestionamento Total", "67,5%", "64,4%", "72,7%", "70,8%", "66,5%", "68,90%"),
    ("DATA_ROW", "Taxa de congestionamento líquida", "65,5%", "66,2%", "70,8%", "74,4%", "69,9%", "66,60%"),
    ("DATA_ROW", "Taxa de congestionamento – 1º grau", "68%", "68%", "74%", "76%", "71%", "71%"),
    ("DATA_ROW", "Taxa de congestionamento – 2º grau", "58%", "53%", "62%", "54%", "52%", "53%"),
    ("DATA_ROW", "Taxa de congestionamento na fase de conhecimento", "66%", "66%", "72%", "74%", "68%", "78%"),
    ("DATA_ROW", "Taxa de congestionamento na fase de execução", "75%", "72%", "79%", "84%", "81%", "67%"),
    ("DATA_ROW", "Índice de recorribilidade interna (Geral)", "9,9%", "9,6%", "12,2%", "12,7%", "s/d", "s/d"),
    ("DATA_ROW", "Índice de recorribilidade externa (Geral)", "7,7%", "7%", "3,8%", "3,6%", "s/d", "s/d"),
    ("DATA_ROW", "Recorribilidade interna – 1º grau (Conhecimento)", "8,2%", "7,9%", "10,7%", "11,2%", "9,5%", "9,5%"),
    ("DATA_ROW", "Recorribilidade interna – 2º grau (**)", "17,9%", "18,7%", "18,7%", "18,3%", "5,3%", "7%"),
    ("DATA_ROW", "Recorribilidade externa – 1º grau (Conhecimento)", "7%", "6%", "3%", "2%", "17,5%", "16,3%"),
    ("DATA_ROW", "Recorribilidade externa – 2º grau (**)", "23%", "22%", "17%", "23%", "0,0%", "0,0%"),
    ("DATA_ROW", "Percentual de casos pendentes de execução em relação ao estoque total de processos", "32,7%", "31,6%", "27,8%", "31,4%", "30,8%", "32,7%"),
    ("DATA_ROW", "Total de execuções fiscais pendentes", "463.524", "423.882", "407.160", "451.845", "396.967", "279.866"),
    ("DATA_ROW", "Taxa de congestionamento na execução fiscal", "74%", "78%", "83%", "86%", "85%", "82%"),
    ("DATA_ROW", "Centros judiciários de solução de conflitos na justiça estadual", "143", "166", "212", "285", "299", "298"),
    ("DATA_ROW", "Índice de conciliação", "19,2%", "16,1%", "13,0%", "12,5%", "14,1%", "13,8%"),
    ("DATA_ROW", "Índice de conciliação, 1º grau", "21,2%", "17,7%", "14,5%", "14,3%", "15,5%", "20,8%"),
    ("DATA_ROW", "Índice de conciliação 2º grau", "0,2%", " 0,2%", "0,2%", "0,5%", "0%", "0,3%"),
    ("DATA_ROW", "Tempo médio até a sentença no 1º grau", "3a e 4m", "3a e 4m", "3a", "2a e 3m", "2a e 3m", "2a e 5m"),
    ("DATA_ROW", "Tempo médio até a sentença no 2º grau", "5m", "8m", "7m", "7m", "5m", "10m"),
    ("DATA_ROW", "Tempo de giro do acervo", "s/d", "2a", "2a e 8m", "2a e 11m", "2a e 4m", "2a e 3m"),
    ("DATA_ROW", "Tempo médio dos processos físicos pendentes", "s/d", "s/d", "s/d", "s/d", "5a e 11m", "7a e 2m"),
    ("DATA_ROW", "Tempo médio dos processos eletrônicos pendentes", "s/d", "s/d", "s/d", "s/d", "2a e 10m", "1a e 11m"),
    ("DATA_ROW", "Casos novos criminais, excluídas as execuções penais", "245.327", "257.645", "211.165", "227.906", "355.278", "411.313"),
    ("DATA_ROW", "Casos pendentes criminais, excluídas as execuções penais", "500.658", "494.353", "524.809", "566.635", "766.828", "627.406"),
    ("DATA_ROW", "Resultado do IPC-Jus total por tribunal (incluída a área administrativa)", "82%", "74%", "77%", "80%", "86%", "61%"),
    ("DATA_ROW", "Resultado do IPC-Jus da área judiciária, por instância e tribunal. 1º grau", "79%", "68%", "73%", "75%", "84%", "56%"),
    ("DATA_ROW", "Resultado do IPC-Jus da área judiciária, por instância e tribunal. 2º grau ", "77%", "83%", "72%", "62%", "68%", "77%"),
    
    # Linhas Complexas com 2 Valores por Ano (Realizado X Necessário/Consequência)
    ("DATA_ROW", "Índice de produtividade dos magistrados (IPM) realizado x necessário para que tribunal atinja IPC-Jus de 100%.", "1.984, 2.384", "2.019, 2.640", "1.471, 1.889", "1.500, 1.853", "1.885, 2.179", "1.906, 3.068"),
    ("DATA_ROW", "Índice de produtividade dos servidores (IPS) realizado x necessário para que tribunal atinja IPC-Jus de 100%.", "124, 149", "127, 166", "99, 127", "104, 128", "123, 143", "126, 203"),
    ("DATA_ROW", "Taxa de congestionamento líquida (TCL) realizado x resultado da consequência se tribunal atingisse IPC-Jus 100%. TCL realizado", "61%, 66%", "58%, 64%", "65%, 71%", "66%, 71%", "64%, 66%", "67%, 56%"),
]

dados_tabela_exemplo_3col = [
    ["HEADER", "PERFORMANCE DO TJMG EM INDICADORES DE ACESSIBILIDADE E INCLUSÃO","",""],
    ["SUB_HEADER", "Categoria", "Status", "Observação"],
    ["DATA_ROW", "Capacitação em Libras", "Excelente", "Líder absoluto em servidores e auxiliares treinados."],
    ["DATA_ROW", "Produção de Vídeos", "Muito Bom", "Alta produção de conteúdo audiovisual acessível."],
    ["DATA_ROW", "Inclusão de Terceirizados", "Muito Bom", "Maior número de terceirizados PCD entre os tribunais de grande porte."],
    ["DATA_ROW", "Eventos Acessíveis", "Atenção", "Baixa proporção de eventos com acessibilidade frente ao total."],
    ["DATA_ROW", "Infraestrutura Física", "Atenção", "Necessidade de capacitar técnicos em normas de acessibilidade."],
    ]

dados_exemplo_4col = [
    ["HEADER", "RESULTADO TJMG COMPARATIVO 2024 X 2025", "", "", ""],
    ["SUB_HEADER", "Indicador", "2024", "2025", "Variação"],
    ["DATA_ROW", "Nota iGovTIC-JUD", "96.19", "84.21", "-11.98"],
    ["DATA_ROW", "Nível de Maturidade", "Excelência", "Aprimorado", "Queda de Nível"],
]

dados_igovtic = [
    ["HEADER", "RESULTADO COMPARATIVO IGOVTIC-JUD NA JUSTIÇA ESTADUAL (GRANDE PORTE)", "", "", "", "", ""],
    ["SUB_HEADER", "Tribunal", "Nota\n2024", "Nível de\nMaturidade (2024)", "Nota\n2025", "Nível de\nMaturidade (2025)", "Variação"],
    ["DATA_ROW", "TJPR", "99,28", "Excelência", "94,41", "Excelência", "-4,87"],
    ["DATA_ROW", "TJSP", "76,67", "Aprimorado", "56,33", "Satisfatório", "-20,34"],
    ["DATA_ROW", "TJBA", "91,62", "Excelência", "88,99", "Aprimorado", "-2,63"],
    ["DATA_ROW", "TJRS", "63,96", "Satisfatório", "76,45", "Aprimorado", "+12,49"],
    ["DATA_ROW", "TJMG", "96,19", "Excelência", "84,21", "Aprimorado", "-11,98"],
    ["DATA_ROW", "TJRJ", "94,09", "Excelência", "92,36", "Excelência", "-1,73"],
]

dados_comparativo_temas = [
    ["HEADER", "COMPARATIVO NA JUSTIÇA ESTADUAL DE GRANDE PORTE DAS NOTAS ALCANÇADAS POR TEMA", "", "", "", "", "", ""],
    ["SUB_HEADER", "TEMAS", "ESTADUAL", "TJSP", "TJRJ", "TJPR", "TJRS", "TJBA", "TJMG"],
    ["SECTION_HEADER", "GOVERNANÇA E GESTÃO DE TIC", "", "", "", "", "", "", ""],
    ["DATA_ROW", "1 - Estruturas Organizacionais e Macroprocessos", "85,56", "50,00", "95,00", "100,00", "81,00", "50,00", "57,50"],
    ["DATA_ROW", "2 - Políticas e Planejamento", "89,61", "7,20", "85,00", "100,00", "81,40", "77,80", "86,80"],
    ["DATA_ROW", "3 - Transformação Digital", "93,08", "48,00", "95,00", "81,75", "77,50", "100,00", "98,75"],
    ["DATA_ROW", "4 - Atendimento e Suporte ao Usuário", "92,52", "100,00", "100,00", "100,00", "64,00", "100,00", "100,00"],
    ["DATA_ROW", "5 - Pessoas", "70,37", "0,00", "80,00", "80,00", "80,00", "80,00", "42,50"],
    ["SECTION_HEADER", "Gerenciamento de Serviços de TIC", "", "", "", "", "", "", ""],
    ["DATA_ROW", "6 - Infraestrutura Tecnológica e Serviços em Nuvem", "89,35", "75,30", "94,90", "99,70", "81,04", "94,30", "99,10"],
    ["DATA_ROW", "7 - Riscos, Segurança da Informação e Proteção de Dados", "91,44", "66,50", "100,00", "100,00", "52,00", "100,00", "75,00"],
    ["DATA_ROW", "8 - Sistemas de Informação", "96,54", "73,75", "100,00", "100,00", "73,75", "100,00", "100,00"],
]

dados_datajud_consistencia = [
    ["HEADER", "PERCENTUAL DE PROCESSOS CONSISTENTES DO TJMG NO DATAJUD", "", "", ""],
    ["SUB_HEADER", "Dados básicos", "Total de\nprocessos", "Processos\ninconsistentes", "% de processos\nconsistentes"],
    ["DATA_ROW", "Flag. Juízo 100% digital", "36.266.191", "9.460.554", "73,91%"],
    ["DATA_ROW", "Assuntos", "36.266.191", "1.918.539", "94,71%"],
    ["DATA_ROW", "Classe processual", "36.266.191", "919.387", "97,46%"],
    ["DATA_ROW", "Identificador procEI", "36.266.191", "40.282", "99,89%"],
    ["DATA_ROW", "Órgão julgador", "36.266.191", "19.065", "99,95%"],
    ["DATA_ROW", "Sistema", "36.266.191", "9.686", "99,97%"],
    ["DATA_ROW", "Data de ajuizamento", "36.266.191", "7.461", "99,98%"],
    ["DATA_ROW", "Prioridade", "4.022.371", "635", "99,98%"],
    ["DATA_ROW", "Custas", "36.266.191", "0", "100,00%"],
    ["DATA_ROW", "Grau", "36.266.191", "0", "100,00%"],
    ["DATA_ROW", "Número", "36.266.191", "0", "100,00%"],
]

dados_desempenho_governanca = [
    ["HEADER", "TABELA COMPARATIVA DE DESEMPENHO DO EIXO GOVERNANÇA", "", "", ""],
    ["SUB_HEADER", "Indicador", "Situação\nAtual", "Meta\nCNJ", "Status"],
    ["DATA_ROW", "IDS (Sustentabilidade)", "62,7%", "> 65%", "⚠️ Crítico"],
    ["DATA_ROW", "Paridade de Gênero", "40%", "49,5%", "⚠️ Crítico"],
    ["DATA_ROW", "Capacitação Acessibilidade", "6,74%", "> 10%", "❌ Não pontuou"],
    ["DATA_ROW", "Inspeções Penais", "93,4%", "100%", "⚠️ Ajuste fino"],
    ["DATA_ROW", "Iper (Equidade Racial)", "28%", "Alinhamento\ncom metas", "⚠️ Crítico"],
]

dados_desempenho_produtividade = [
    ["HEADER", "TABELA COMPARATIVA DE DESEMPENHO DO EIXO PRODUTIVIDADE", "", "", ""],
    ["SUB_HEADER", "Indicador Crítico", "Valor\nAtual", "Meta para\nPontuar", "Impacto"],
    ["DATA_ROW", "Meta 1", "99,69%", "100%", "Altíssimo"],
    ["DATA_ROW", "Medidas Protetivas", "5 dias", "2 dias", "Urgente"],
    ["DATA_ROW", "Adoção (Prazos)", "53,25%", "80%", "Social/Jurídico"],
    ["DATA_ROW", "Incidentes Vencidos", "1,93%", "< 0,10%", "Correcional"],
]

dados_desempenho_transparencia = [
    ["HEADER", "TABELA COMPARATIVA DE DESEMPENHO DO EIXO TRANSPARÊNCIA", "", "", ""],
    ["SUB_HEADER", "Indicador", "Status\nAtual", "Meta CNJ\n2025", "Impacto na\nPontuação"],
    ["DATA_ROW", "Ranking da Transparência", "91,6%", "≥ 95%", "0 pontos (Atualmente)"],
    ["DATA_ROW", "Gap de Conformidade", "-3,4%", "100%", "Pontuação Máxima"],
]

dados_desempenho_tecnologia = [
    ["HEADER", "TABELA COMPARATIVA DE DESEMPENHO DO EIXO DADOS E TECNOLOGIA", "", "", ""],
    ["SUB_HEADER", "Requisito", "Situação\nAtual", "Meta\nCNJ", "Ação Corretiva"],
    ["DATA_ROW", "Documentação (CPF/CNPJ)", "84% - 86%", "95%", "Força-tarefa de saneamento no cadastro inicial"],
    ["DATA_ROW", "Identificação Magistrado", "52%", "90%", "Configuração compulsória de CPF no login/assinatura"],
    ["DATA_ROW", "Processos Eletrônicos", "97,93%", "98,01%", "Digitalização/Baixa dos últimos acervos físicos"],
    ["DATA_ROW", "Órgão Colegiado", "1%", "90%", "Parametrização dos sistemas de 2º Grau"],
    ["DATA_ROW", "Corpo Técnico TI", "205", "234", "Concurso público ou redistribuição de cargos"],
]

dados_tabela_metas_consolidadas = [
    ("HEADER", "Metas Nacionais para a Justiça Estadual"),
    ("SUB_HEADER", "Meta Nacional", "Índice de Cumprimento Alcançado", "Síntese das ações Específicas de Melhoria Citadas pelos Tribunais"),
    ("DATA_ROW", "Meta 1\nJulgar mais processos que os distribuídos", "99,69%", "Indicador em consolidação para 2025. Necessário implementar processos de\npriorização e especialização das câmaras."),
    ("DATA_ROW", "Meta 2\nJulgar processos mais antigos", "105,83%", "Excelente desempenho com foco em processos de execução e demandas estruturais."),
    ("DATA_ROW", "Meta 3\nEstimular a conciliação", "100,00%", "Meta atingida atrav és de núcleos de mediação e mediação judicial."),
    ("DATA_ROW", "Meta 4\nPrioritizar crimes contra Administração Pública,\nimprobidade e ilícitos eleitorais", "133,80%", "Desempenho excepcional com priorização de ações de combate à corrupção\ne ilícitos eleitorais."),
    ("DATA_ROW", "Meta 5\nReduzir taxa de congestionamento", "84,41%", "Redução estratégica de 0,5% ao ano. Foco em digitalização e eficiência nos\nprocessos de 1º grau."),
    ("DATA_ROW", "Meta 6\nPrioritizar julgamento de ações ambientais", "50,00%", "Meta em implementação. Foco em demandas ambientais de importância\nregional e estadual."),
    ("DATA_ROW", "Meta 7\nPrioritizar julgamento de processos com indígenas\ne quilombolas", "285,71%", "Desempenho excepcional com especialização de câmaras e magistrados\ntreinados em temas sensíveis."),
    ("DATA_ROW", "Meta 8\nPrioritizar violência doméstica e feminicídio", "109,26%", "Desempenho acima da meta. Núcleos especializados e protocolos\nacel erados para proteção integral."),
    ("DATA_ROW", "Meta 9\nEstimular inovação no Poder Judiciário", "100,00%", "Implementação de Núcleos de Justiça 4.0 com foco em inovação processual\ne aceleração de julgamentos."),
]


dados_tabela_premio_cnj = [
    ("HEADER", "PRÊMIO CNJ DE QUALIDADE – PONTUAÇÃO GERAL TJMG: 52,1%"),
    ("SUB_HEADER", "EIXO", "PONTUAÇÃO"),
    ("DATA_ROW", "Governança", "68,1%"),
    ("DATA_ROW", "Produtividade", "34,0%"),
    ("DATA_ROW", "Transparência", "28,6%"),
    ("DATA_ROW", "Dados e Tecnologia", "61,4%"),
]


HISTORICO_METAS_CNJ = {
    "Meta 1": {
        "descricao": "Julgar mais processos que os distribuídos",
        "objetivo": ">100%",
        "dados_passados": {
            # Listas agora com 4 valores (2021, 2022, 2023, 2024)
            "Total": ["101,27%", "99,19%", "204,83%", "117,70%"],
            "1º Grau":          ["98,03%", "97,90%", "260,77%", "129,50%"],
            "2º Grau":          ["101,41%", "108,86%", "126,72%", "90,09%"],
            "Juizado Especial": ["117,38%", "102,67%", "199,01%", "132,57%"],
            "Turma Recursal":   ["70,37%", "70,05%", "171,62%", "84,76%"]
        }
    },
    "Meta 2": {
        "descricao": "Julgar processos mais antigos",
        "objetivos_anos": [
            "80% 1º Grau\n90% Demais", 
            "80% 1º Grau\n90% Demais", 
            "80% 1º Grau\n90% Demais", 
            "80% 1º Grau\n90% Demais\n100% Mais antigos",
            "80% 1º Grau\n90% Demais\n100% Mais antigos"
        ],
        "dados_passados": {
            "1º Grau":          ["104,81%", "89,52%", "122,78%", "105,83%"],
            "2º Grau":          ["122,96%", "122,64%", "109,70%", "85,54%"],
            "Juizado Especial": ["107,79%", "102,79%", "109,29%", "101,82%"],
            "Turma Recursal":   ["104,25%", "68,02%", "110,29%", "106,96%"],
            "Mais antigos":     ["-", "-", "-", "38,06%"]
        }
    },
    "Meta 3": {
        "descricao": "Estimular a conciliação",
        # Omitimos 'objetivo' pois não há linha de meta fixa
        "dados_passados": {
            # Histórico de 2021 a 2024
            "Tribunal": ["93,64%", "105,04%", "100,00%", "100,00%"]
        }
    },
    "Meta 4": {
        "descricao": "Priorizar o julgamento dos processos relativos aos crimes contra a Administração Pública, à improbidade administrativa e aos ilícitos eleitorais",
        "grupos": [
            {
                "nome": "Crimes Contra Administração Pública",
                "objetivos_anos": ["70%", "70%", "60%", "65%", "65%"],
                "chave_busca": "Crimes Contra Adm.",
                "dados": {
                    "Geral":            ["102,44%", "130,38%", "149,81%", "133,80%"],
                    "1º Grau":          ["102,36%", "125,31%", "149,19%", "125,64%"],
                    "2º Grau":          ["114,64%", "163,52%", "151,75%", "151,06%"],
                    "Juizado Especial": ["142,86%", "166,67%", "151,65%", "141,50%"],
                    "Turma Recursal":   [ "-", "-", "153,85%", "149,82%"]                }
            },
            {
                "nome": "Improbidade Administrativa",
                "chave_busca": "Improbidade",
                "objetivos_anos": ["-", "-", "-", "-", "100%"],
                "dados": {
                    "Geral":            ["-", "-", "-", "-"],
                    "1º Grau":          ["-", "-", "-", "-"],
                    "2º Grau":          ["-", "-", "-", "-"],
                    "Juizado Especial": ["-", "-", "-", "-"],
                    "Turma Recursal":   ["-", "-", "-", "-"]                }
            }
        ]
    },
    "Meta 5": {
        "descricao": "Reduzir a taxa de congestionamento",
        "objetivos_anos": [
            "Redução 2%", 
            "Redução 0,5%", 
            "Redução 0,5%", 
            "Redução 0,5%",
            "Redução 0,5%"
        ],
        "dados_passados": {
            "Total":              ["117,48%", "102,63%", "**", "84,41%"],
            "1º Grau":            ["-", "-", "**", "86,70%"],
            "2º Grau":            ["-", "-", "**", "72,57%"],
            "Juizado Especial":   ["-", "-", "**", "85,92%"],
            "Turma Recursal":     ["-", "-", "**", "60,88%"]
        }
    },
    "Meta 6": {
        "descricao": "Priorizar o julgamento das ações ambientais",
        "objetivos_anos": [
            "-", 
            "-", 
            "-", 
            "-", 
            "50%"
        ],
        "dados_passados": {
            "Total":              ["-", "-", "-", "-"],
            "1º Grau":            ["-", "-", "-", "-"],
            "2º Grau":            ["-", "-", "-", "-"],
            "Juizado Especial":   ["-", "-", "-", "-"],
            "Turma Recursal":     ["-", "-", "-", "-"]
        }
    },
    "Meta 7": {
        "descricao": "Priorizar o julgamento dos processos relacionados aos indígenas e quilombolas",
        "objetivos_anos": [
            "-", 
            "-", 
            "-", 
            "35%", 
            "50%"
        ],
        "dados_passados": {
            "Total Indígenas":    ["-", "-", "-", "-"],
            "Total Quilombola":  ["-", "-", "-", "285,71%"]        }
    },
    "Meta 8": {
        "descricao": "Priorizar o julgamento dos processos relacionados ao feminicídio e à violência doméstica e familiar contra as mulheres",
        "grupos": [
            {
                "nome": "Violência Doméstica",
                "objetivos_anos": ["50%", "50%", "50%", "75%", "75%"],
                "chave_busca": "Violência Doméstica",
                "dados": {
                    "Total":            ["140,37%", "110,83%", "195,14%", "109,26%"],
                    "1º Grau":          ["138,97%", "68,87%", "193,46%", "95,18%"],
                    "2º Grau":          ["200,00%", "198,04%", "151,75%", "130,48%"]     }
            },
            {
                "nome": "Feminicídio",
                "chave_busca": "Feminicídio",
                "objetivos_anos": ["50%", "50%", "60%", "90%", "90%"],
                "dados": {
                    "Total":            ["128,38%", "143,51%", "162,74%", "92,15%"],
                    "1º Grau":          ["124,06%", "143,11%", "162,65%", "91,53%"],
                    "2º Grau":          ["199,69%", "165,67%", "166,04%", "107,76%"],
                    "Juizado Especial": ["-", "-", "156,49%", "79,27%"]                }
            }
        ]
    },
    "Meta 9": {
        "descricao": "Estimular a inovação no Poder Judiciário",
        # Omitimos 'objetivo' pois não há linha de meta fixa
        "dados_passados": {
            # Histórico de 2021 a 2024
            "Tribunal": ["100,00%", "100,00%", "100,00%", "100,00%"]
        }
    },
    "Meta 10": {
        "descricao": "Promover os direitos da criança e do adolescente",
        "objetivos_anos": [
            "-", 
            "80% 1º Grau \n95% 2º Grau", 
            "80% 1º Grau \n95% 2º Grau", 
            "90% 1º Grau \n100% 2º Grau", 
            "90% 1º Grau \n100% 2º Grau"
        ],
        "dados_passados": {
            "1º Grau":    ["-", "-", "118,63%", "82,74%"],
            "2º Grau":    ["-", "101,98%", "104,49%", "97,13%"]        }
    },
}

MAPA_RECURSOS = {

    ########################################################################
    ########################################################################
    #########################------TABELAS------############################
    ########################################################################
    ########################################################################

    "Tabela 01 - Atos Normativos referentes à Estrutura do TJMG.": {
        "tipo": "TABELA_GENERICA",
        "dados": dados_tabela_atos,
        "fonte_custom": "Portal TJMG",
        "space_after": 20
    },
    "Tabela 02 - Principais áreas da Secretaria do TJMG": {
        "tipo": "TABELA_AREAS",
        "dados": dados_tabela_areas,
        "space_after": 20
    },
    "Tabela 03 - Estrutura para a prestação jurisdicional na Segunda Instância": {
        "tipo": "TABELA_ESTRUTURA",
        "dados": dados_tabela_estrutura,
        "space_after": 20
    },
    "Tabela 04 - Estrutura para a prestação jurisdicional na Primeira Instância. Listagem das Comarcas Instaladas em Minas Gerais": {
        "tipo": "TABELA_COMARCAS",
        "dados": dados_tabela_comarcas,
        "space_after": 20
    },
    "Tabela 05 - Relação dos Núcleos de Justiça 4.0 da Primeira Instância": {
        "tipo": "TABELA_NUCLEOS",
        "dados": dados_tabela_nucleos,
        "space_after": 20
    },
    "Tabela 06 - Número de processos distribuídos": {
        "tipo": "TABELA_PROCESSOS",
        "dados": dados_tabela_processos,
        "space_after": 20
    },
    "Tabela 07 - Julgamentos Realizados": {
        "tipo": "TABELA_PROCESSOS",
        "dados": dados_tabela_julgamentos,
        "space_after": 20
    },
    "Tabela 08 - Dados do Acervo": {
        "tipo": "TABELA_PROCESSOS",
        "dados": dados_tabela_acervo,
        "space_after": 20
    },
    "Tabela 09 - Despesa realizada por ação (Unidade 1031)": {
        "tipo": "TABELA_ORCAMENTO",
        "dados": dados_tabela_orcamento,
        "num": "09",
        "fonte_custom": "Armazém de Informações - BO SIAFI/MG",
        "titulo": TITULO_TABELA_ORCAMENTO_1,
        "space_after": 6
    },
    "Tabela 10 - Despesa realizada por ação (Unidade 4031)": {
        "tipo": "TABELA_ORCAMENTO", # Ou usar TABELA_ORCAMENTO com num="11"
        "dados": dados_tabela_orcamento_acao,
        "num": "10",
        "fonte_custom": "Armazém de Informações - BO SIAFI/MG",
        "titulo": TITULO_TABELA_ORCAMENTO_2,
        "space_after": 6
    },
    "Tabela 11 - Orçamento 2026 por ação orçamentária": {
        "tipo": "TABELA_ORCAMENTO_CONJUNTO", # Ou usar TABELA_ORCAMENTO com num="11"
        "dados": dados_tabela_orcamento_2025,
        "fonte_custom": "Fonte: Lei Orçamentária Anual nº 25.698, de 14/01/2026.",
        "titulo": TITULO_TABELA_ORCAMENTO_ACAO,
        "space_after": 20
    },
    "Tabela 12 - Comparativo Orçamento 2025 x 2026 por ação orçamentária": {
        "tipo": "TABELA_ORCAMENTO_CONJUNTO_COMPARACAO",
        "dados": dados_tabela_orcamento_comparacao,
        "fonte_custom": "Fonte: LOA/TJMG.",
        "space_after": 20
    },
    "Tabela - Cidades": {
        "tipo": "TABELA_CIDADES", 
        "dados": dados_tabela_cidades,
        "space_after": 20
    },
    "Tabela 13 - Resultado Consolidado das Metas Nacionais para a Justiça Estadual.": {
        "tipo": "TABELA_METAS_CONSOLIDADAS",
        "dados": dados_tabela_metas_consolidadas,
        "fonte_custom": "Fonte: Metas Nacionais do Poder Judiciário/CNJ.",
        "recuo_esq": 0,
        "space_after": 20
    },
    "Tabela 14: Performance do TJMG em indicadores de acessibilidade e inclusão.": {
        "tipo": "TABELA_SIMPLES_3COL", 
        "dados": dados_tabela_exemplo_3col,
        "fonte_custom": "Fonte: Painel de Sustentabilidade do CNJ.",
        "recuo_esq": 0,
        "space_after": 20
    },
    "Tabela 15: Resultado TJMG comparativo 2024 X 2025.": {
        "tipo": "TABELA_4COL_SIMPLES", 
        "dados": dados_exemplo_4col,
        "fonte_custom": "Fonte: Painel iGovTIC-JUD CNJ.",
        "recuo_esq": -0.5, 
        "space_after": 20
    },
    "Tabela 16 - Resultado comparativo do iGovTIC-JUD na Justiça Estadual de grande porte.": {
        "tipo": "TABELA_6COL_SIMPLES",
        "dados": dados_igovtic,
        "fonte_custom": "Fonte: Levantamento de Governança, Gestão e Infraestrutura de TIC do Poder Judiciário – agosto 2025/CNJ.",
        "recuo_esq": -0.5, # Um pequeno recuo para a esquerda ajuda tabelas largas
        "space_after": 20
    },
    "Tabela 17 - Comparativo na Justiça Estadual de Grande Porte das notas alcançadas por tema.": {
        "tipo": "TABELA_COMPARATIVO_TEMAS",
        "dados": dados_comparativo_temas,
        "fonte_custom": "Fonte: Levantamento de Governança, Gestão e Infraestrutura de TIC do Poder Judiciário – agosto 2025/CNJ.",
        "recuo_esq": -0.5, # Ajuste para caber bem na página
        "space_after": 20
    },
    "Tabela 18 - Tabela percentual de processos consistentes do TJMG no Datajud.": {
        "tipo": "TABELA_4COL_SIMPLES",
        "dados": dados_datajud_consistencia,
        "fonte_custom": "Fonte Painel Qualidade dos dados/ CNJ atualizado em 01/02/2026",
        "recuo_esq": -0.5, # Ajuste para caber bem na página
        "space_after": 20
    },
    "Tabela 19 - Pontuação do TJMG na edição 2025 do Prêmio CNJ de Qualidade.": {
        "tipo": "TABELA_2COL",
        "dados": dados_tabela_premio_cnj,
        "fonte_custom": "Fonte: Painel de resultados do Prêmio/CNJ.",
        "recuo_esq": 0,
        "space_after": 20
    },
    "Tabela 20 - Tabela comparativa de Desempenho do Eixo Governança.": {
        "tipo": "TABELA_4COL_SIMPLES",
        "dados": dados_desempenho_governanca,
        "fonte_custom": "Fonte: Painel de resultados do Prêmio/ CNJ.",
        "recuo_esq": -0.5,
        "space_after": 20
    },
    "Tabela 21 - Tabela comparativa de Desempenho do Eixo Produtividade.": {
        "tipo": "TABELA_4COL_SIMPLES",
        "dados": dados_desempenho_produtividade,
        "fonte_custom": "Fonte: Painel de resultados do Prêmio/ CNJ.",
        "recuo_esq": -0.5,
        "space_after": 20
    },
    "Tabela 22 - Tabela comparativa de Desempenho do Eixo Transparência.": {
        "tipo": "TABELA_4COL_SIMPLES",
        "dados": dados_desempenho_transparencia,
        "fonte_custom": "Fonte: Painel de resultados do Prêmio CNJ.",
        "recuo_esq": -0.5,
        "space_after": 20
    },
    "Tabela 23 - Tabela comparativa de Desempenho do Eixo Dados e Tecnologia.": {
        "tipo": "TABELA_4COL_SIMPLES",
        "dados": dados_desempenho_tecnologia,
        "fonte_custom": "Fonte: Painel de resultados do Prêmio CNJ.",
        "recuo_esq": -0.5,
        "space_after": 20,
        "larguras": [2400, 1300, 1300, 4600] 
    },
    

    ########################################################################
    ########################################################################
    ####################-------METAS NACIONAIS-------#######################
    ########################################################################
    ########################################################################

    "Meta 1": {
    "tipo": "TABELA_METAS_DINAMICA",
    "recuo_esq": -1.4,
    "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 2": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 3": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 4": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.6,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 5": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 6": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 7": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 8": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 9": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.4,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },
    "Meta 10": {
        "tipo": "TABELA_METAS_DINAMICA",
        "recuo_esq": -1.6,
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },

    # === TODAS AS METAS INSTITUCIONAIS (SEÇÃO UNIFICADA) ===
    "METAS_INSTITUCIONAIS": {
        "tipo": "METAS_INSTITUCIONAIS",
        "fonte_custom": "Fonte: Painel Metas Nacionais CNJ,  acessado em 28/01/2026. *Dados até 31/12/2025."
    },

    ########################################################################
    ########################################################################
    #########################------IMAGENS------############################
    ########################################################################
    ########################################################################

    "Figura 01 - Informações sobre o Estado de Minas Gerais.": {
        "tipo": "IMAGEM", "arquivo": "figura_01.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 17.69,
        "recuo_esq": -0.85,
        "space_after": 20
    },
    "Figura 02 - Síntese da estrutura na área fim.": {
        "tipo": "IMAGEM", "arquivo": "figura_02.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 17.69,
        "recuo_esq": -0.95,
        "space_after": 20
    },
    "Figura 03 - Novas estruturas na área fim.": {
        "tipo": "IMAGEM", "arquivo": "figura_03.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 18.56,
        "recuo_esq": -1.35,
        "space_after": 20
    },
    "Figura 04 - Força de Trabalho.": {
        "tipo": "IMAGEM", "arquivo": "figura_04.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 17.00,
        "space_after": 24,
        "recuo_esq": -1.35,
        "space_after": 20  
    },
    "Figura 05 - Colaboradores da Justiça.": {
        "tipo": "IMAGEM", "arquivo": "figura_05.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 17.00,
        "recuo_esq": -1.35,
        "space_after": 20
    },
    "Figura 06 – Força de Trabalho e Colaboradores na área de TI.": {
        "tipo": "IMAGEM", "arquivo": "figura_06.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "largura": 17.00,
        "recuo_esq": -1.35,
        "space_after": 20
    },
    "Figura 07 - Grandes Litigantes Polo Passivo.": {
        "tipo": "IMAGEM", "arquivo": "figura_07.png",
        "fonte" : "Fonte: Painel Litigantes do CNJ",
        "largura": 12.50,
        "space_after": 20
    },
    "Figura 08 - Grandes Litigantes Polo Ativo.": {
        "tipo": "IMAGEM", "arquivo": "figura_08.png",
        "fonte" : "Fonte: Painel Litigantes do CNJ",
        "largura": 12.50,
        "space_after": 20
    },
    "Figura 09 - Instalações prediais do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "figura_09.png",
        "fonte" : "Fonte: Centro de Informações para a Gestão Institucional – CEINFO",
        "space_after": 20
    },
    "Figura 10 - Desempenho da ação por programa (Unidade 1031).": {
        "tipo": "IMAGEM", "arquivo": "figura_10.png",
        "fonte" : "Fonte: Sigplan",
        "largura": 19.0,
        "recuo_esq": -1.85,
        "space_after": 20
    },
    "Figura 11 - Desempenho da ação por programa (Unidade 4031).": {
        "tipo": "IMAGEM", "arquivo": "figura_11.png",
        "fonte" : "Fonte: Sigplan",
        "largura": 19.0,
        "recuo_esq": -1.85,
        "space_after": 20
    },
    "Figura 12 - Esquema do Plano Estratégico 2025.": {
        "tipo": "IMAGEM", "arquivo": "figura_12.png",
        "fonte" : "Fonte: Sigplan",
        "largura": 18.0,
        "recuo_esq": -1,
        "space_after": 30,
        "space_after": 20
    },
    "Figura 13 - Identidade organizacional do TJMG/DIRCOM": {
        "tipo": "IMAGEM", "arquivo": "figura_13.png",
        "fonte" : "Fonte: Sigplan",
        "largura": 13.0,
        "space_after": 30,
        "space_after": 20
    },
    "Figura 14 - Mapa Estratégico do TJMG/ DIRCOM": {
        "tipo": "IMAGEM", "arquivo": "figura_14.png",
        "fonte" : "Fonte: Sigplan",
        "largura": 13.0,
        "space_after": 30,
        "space_after": 20
    },
    "Figura 15 - ODS/ONU.": {
        "tipo": "IMAGEM", "arquivo": "figura_15.png",
        "fonte" : "Fonte: https://brasil.un.org/pt-br/sdgs",
        "largura": 16.0,
        "recuo_esq": 0,
        "space_after": 40,
        "space_after": 20
    },
    "Figura 16 - Composição da Matriz de Priorização de Iniciativas do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "figura_16.png",
        "fonte" : "Fonte: ASPLAG/DEPLAG",
        "largura": 16.0,
        "recuo_esq": 0,
        "space_after": 40,
        "space_after": 20
    },
    "Figura 17 - Grupos de interesse do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "figura_17.png",
        "fonte" : "Fonte: : Assessoria Técnica e Jurídica ao Planejamento e à Gestão Institucional – ASPLAG.",
        "largura": 11.0,
        "recuo_esq": 2.0,
        "space_after": 40,
        "space_after": 20
    },
    "Figura 18 - Habitantes por varas e juizado especial da Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "figura_18.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 11.0,
        "recuo_esq": 2.0,
        "space_after": 40,
        "space_after": 20
    },
    "Figura 19 - Receita x Despesa – TJMG e Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "figura_19.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 17.0,
        "recuo_esq": -1.0,
        "space_after": 30,
        "space_after": 20
    },
    "Figura 20 - Classificação dos tribunais da Justiça Estadual segundo o porte, ano-base 2024.": {
        "tipo": "IMAGEM", "arquivo": "figura_20.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 30,
        "space_after": 20
    },
    "Foto 01 - Participantes do Programa ESG no TJMG treinados como multiplicadores.": {
        "tipo": "IMAGEM", "arquivo": "foto_01.png",
        "fonte" : "Fonte: EJEF.",
        "largura": 18.0,
        "recuo_esq": -0.5,
        "space_after": 30,
        "space_after": 20
    }, 
    


    ########################################################################
    ########################################################################
    ##########################-----GRÁFICOS-----############################
    ########################################################################
    ########################################################################

    "Gráfico 01 - Perfil racial no Poder Judiciário.": {
        "tipo": "IMAGEM", "arquivo": "grafico_01.png",
        "fonte" : "Fonte: Diagnóstico Étnico-Racial no Poder Judiciário.",
        "largura": 12.50,
        "space_after": 20
    },
    "Gráfico 02 - Percentual de magistrados(as) negros(as) na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_02.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 12.50,
        "space_after": 20
    },
    "Gráfico 03 - Percentual de magistrados(as) na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_03.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 12.50,
        "space_after": 20
    },
    "Gráfico 04 - Percentual de Desembargadoras na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_04.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 12.50,
        "space_after": 20
    },
    "Gráfico 05 - Número de municípios-sede e unidades judiciárias por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_05.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 06 - Evolução das receitas totais e das despesas totais do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_06.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 07 - Evolução da despesa total com pessoal do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_07.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.0,
        "space_after": 20
    },
    "Gráfico 08 - Custo médio mensal nos Tribunais de Justiça de grande porte com magistrados(as) e servidores(as), incluindo benefícios, encargos, previdência social, diárias, passagens, indenizações judiciais e demais indenizações eventuais e não eventuais.": {
        "tipo": "IMAGEM", "arquivo": "grafico_08.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 09 - Valores arrecadados em relação ao número de processos ingressados no TJMG e na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_09.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 10 - Arrecadação com custas x Despesas totais no TJMG e Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_10.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.25,
        "space_after": 20
    },
    "Gráfico 11 - Assistência Judiciária Gratuita no TJMG e na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_11.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 12 - Número de CEJUSCs por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_12.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.25,
        "space_after": 20
    },
    "Gráfico 13 - Evolução de casos novos no TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_13.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 17.5,
        "recuo_esq": -0.85,
        "space_after": 20
    },
    "Gráfico 14 - Variação de casos novos – 2023 – 2024 TJMG e Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_14.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 15 - Magistrados por 100 mil habitantes e percentual de cargos vagos de magistrados.": {
        "tipo": "IMAGEM", "arquivo": "grafico_15.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 16 - Percentual de servidores lotados na área administrativa.": {
        "tipo": "IMAGEM", "arquivo": "grafico_16.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 17 - IPC-Jus dos tribunais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_17.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 18 - Análise de cenário para alcançar 100% no IPC-JUS dos tribunais estaduais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_18.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 19 - Evolução dos processos baixados do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_19.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 17.0,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 20 - Ranking de processos baixados em 2024 na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_20.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 21 - Tempo médio dos processos baixados e pendentes nos tribunais estaduais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_21.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 22 - Evolução do Índice de Atendimento à Demanda do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_22.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 17.0,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 23 - Ranking do índice de Atendimento à Demanda dos tribunais estaduais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_23.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 24 - Evolução da Taxa de Congestionamento Total e Líquida do TJMG.": {
        "tipo": "IMAGEM", "arquivo": "grafico_24.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 25 - Taxa de Congestionamento Total na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_25.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 26 - Taxa de Congestionamento Líquida na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_26.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 27 - Índice de Conciliação e sua trajetória no tempo para o TJMG e para a Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_27.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 17.5,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 28 - Processos pendentes de execução fiscal e tempo de tramitação na execução fiscal nos tribunais de justiça de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_28.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 29 - Despesa com recursos humanos por tribunais estaduais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_29.png",
        "fonte" : "Fonte: “Justiça em Números 2025” – Ano base 2024/ CNJ.",
        "largura": 17.0,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 30 - Percentual de servidores lotados na área administrativa.": {
        "tipo": "IMAGEM", "arquivo": "grafico_30.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 17.0,
        "recuo_esq": -0.75,
        "space_after": 20
    },
    "Gráfico 31 - Valores arrecadados em relação ao número de processos ingressados sujeitos a cobrança.": {
        "tipo": "IMAGEM", "arquivo": "grafico_31.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 32 - Índice de conciliação por Tribunal de Justiça.": {
        "tipo": "IMAGEM", "arquivo": "grafico_32.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 33 - Percentual de audiências de conciliação por casos novos por Tribunal de Justiça.": {
        "tipo": "IMAGEM", "arquivo": "grafico_33.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 34 - Percentual de execuções fiscais pendentes em relação ao total de processos pendentes.": {
        "tipo": "IMAGEM", "arquivo": "grafico_34.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 35 - Resultado do IPC-Jus da área judiciária por instância e Tribunal de Justiça.": {
        "tipo": "IMAGEM", "arquivo": "grafico_35.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 36 - IPC-Jus dos tribunais de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_36.png",
        "fonte" : "Fonte: ‘Justiça em Números 2025’ – Ano base 2024/ CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 37 - Tempo de giro do acervo, por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_37.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 38 - Tempo médio de tramitação dos processos pendentes e baixados, por Tribunal de Justiça.": {
        "tipo": "IMAGEM", "arquivo": "grafico_38.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 39 - Taxa de congestionamento, por tribunal de justiça de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_39.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 40 - Taxa de congestionamento na execução fiscal, por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_40.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 41 - Índice de produtividade dos magistrados, por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_41.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 42 - Índice de produtividade dos servidores da área judiciária, por tribunal de grande porte.": {
        "tipo": "IMAGEM", "arquivo": "grafico_42.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 43 - Custo médio mensal nos Tribunais de Justiça com magistrados(as) e servidores(as).": {
        "tipo": "IMAGEM", "arquivo": "grafico_43.png",
        "fonte" : "Fonte: Relatório Justiça em Números – 2025/CNJ.",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 44 - Ranking da Transparência na Justiça Estadual.": {
        "tipo": "IMAGEM", "arquivo": "grafico_44.png",
        "fonte" : "Fonte: Painel com resultado final de todos os tribunais e conselhos/ CNJ",
        "largura": 18.0,
        "recuo_esq": -1.1,
        "space_after": 20
    },
    "Gráfico 45 - Performance do TJMG no Prêmio CNJ de Qualidade - Governança.": {
        "tipo": "IMAGEM", "arquivo": "grafico_45.png",
        "fonte" : "Fonte: Painel de resultados do prêmio/ CNJ.",
        "largura": 14.0,
        "recuo_esq": -0.7,
        "space_after": 20
    },
    "Gráfico 46 - Performance do TJMG no Prêmio CNJ de Qualidade - Produtividade.": {
        "tipo": "IMAGEM", "arquivo": "grafico_46.png",
        "fonte" : "Fonte: Painel de resultados do prêmio/ CNJ.",
        "largura": 14.0,
        "recuo_esq": -0.7,
        "space_after": 20
    },
    "Gráfico 47 - Performance do TJMG no Prêmio CNJ de Qualidade - Dados e Tecnologia.": {
        "tipo": "IMAGEM", "arquivo": "grafico_47.png",
        "fonte" : "Fonte: Painel de resultados do prêmio/ CNJ.",
        "largura": 14.0,
        "recuo_esq": -0.7,
        "space_after": 20
    },
    "Gráfico 48 - Performance do TJMG no Prêmio CNJ de Qualidade - Transparência.": {
        "tipo": "IMAGEM", "arquivo": "grafico_48.png",
        "fonte" : "Fonte: Painel de resultados do prêmio/ CNJ.",
        "largura": 14.0,
        "recuo_esq": -0.7,
        "space_after": 20
    },

}




