"""
Script para gerar o CSV de diálogo com quoting correto.
Execute: python backend/generate_dialogue_csv.py
"""
import csv
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_docs", "Dialogo_Base_Conhecimento_IA.csv")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

ROWS = [
    # setor, intencao, pergunta, resposta, palavras_chave, confianca
    ("Recursos Humanos", "politica_home_office",
     "Qual é a política de home office da empresa?",
     "Todos os colaboradores têm direito a 3 dias de trabalho remoto por semana. O auxílio-home office mensal é de R$ 350,00 para cobrir despesas com internet e energia elétrica. O colaborador deve manter disponibilidade via Slack nos horários comerciais.",
     "home office trabalho remoto auxilio", "Alta"),

    ("Recursos Humanos", "politica_home_office",
     "Quantos dias de home office tenho direito?",
     "Você tem direito a 3 dias de trabalho remoto por semana conforme a Política de Trabalho Híbrido vigente. Os dias devem ser combinados com sua liderança com pelo menos 48h de antecedência.",
     "home office dias direito", "Alta"),

    ("Recursos Humanos", "beneficios",
     "Qual é o plano de saúde oferecido pela empresa?",
     "A empresa oferece plano de saúde Bradesco Top Nacional sem coparticipação para o titular. Dependentes podem ser incluídos com desconto de 30% na mensalidade. O plano cobre consultas, exames e internações em todo o território nacional.",
     "plano saude bradesco beneficio", "Alta"),

    ("Recursos Humanos", "beneficios",
     "Qual o valor do vale refeição?",
     "O vale refeição/alimentação é disponibilizado via cartão Flash no valor de R$ 1.200,00 mensais. O saldo é creditado no primeiro dia útil de cada mês e pode ser utilizado em restaurantes, supermercados e delivery.",
     "vale refeicao alimentacao flash", "Alta"),

    ("Recursos Humanos", "ferias",
     "Como solicitar férias?",
     "As férias devem ser solicitadas no portal de RH com antecedência mínima de 30 dias após completar o período aquisitivo de 12 meses. A aprovação fica sujeita ao gestor imediato em até 5 dias úteis.",
     "ferias solicitar portal", "Alta"),

    ("Recursos Humanos", "ferias",
     "Qual o período aquisitivo de férias?",
     "O período aquisitivo de férias é de 12 meses de trabalho contínuo. Após esse período o colaborador tem direito a 30 dias de descanso remunerado conforme a CLT. É possível fracionar as férias em até 3 períodos.",
     "periodo aquisitivo ferias clt", "Alta"),

    ("Recursos Humanos", "onboarding",
     "Qual o processo de onboarding para novos colaboradores?",
     "O onboarding tem duração de 30 dias. Na primeira semana o colaborador recebe os equipamentos e acesso aos sistemas. Nas semanas 2-4 realiza treinamentos obrigatórios e se integra ao time. O canal principal de comunicação é o Slack.",
     "onboarding novo colaborador integracao", "Alta"),

    ("Recursos Humanos", "salario",
     "Qual a data de pagamento do salário?",
     "O salário é depositado todo dia 5 de cada mês. Em meses com feriados o pagamento é antecipado para o dia útil anterior. O 13º salário é pago em duas parcelas: 50% em novembro e 50% em dezembro.",
     "salario pagamento data", "Alta"),

    ("Recursos Humanos", "treinamento",
     "Quais treinamentos são obrigatórios?",
     "Os treinamentos obrigatórios são: Segurança da Informação e LGPD (anual); Código de Ética e Conduta (anual); e Prevenção ao Assédio (semestral). Todos estão disponíveis na plataforma EAD interna.",
     "treinamento obrigatorio lgpd etica", "Alta"),

    ("Recursos Humanos", "home_office",
     "Qual o valor do auxílio home office mensal?",
     "O auxílio-home office mensal é de R$ 350,00 (trezentos e cinquenta reais) pago junto ao salário do mês referência. É destinado ao custeio de internet banda larga e energia elétrica necessárias para o trabalho remoto.",
     "auxilio home office valor mensal", "Alta"),

    ("Financeiro e Contábil", "dre",
     "Qual foi o lucro líquido no Q4 de 2025?",
     "O lucro líquido no Q4 de 2025 foi de R$ 8.200.000,00. A receita bruta no mesmo trimestre atingiu R$ 18.100.000,00 representando crescimento de 14,6% em relação ao Q3. Os custos operacionais OCI Cloud foram de R$ 1.500.000,00.",
     "lucro liquido Q4 2025 financeiro", "Alta"),

    ("Financeiro e Contábil", "dre",
     "Qual a receita bruta anual de 2025?",
     "A receita bruta total de 2025 somou R$ 60.600.000,00 divididos por trimestre: Q1 R$ 12.500.000 / Q2 R$ 14.200.000 / Q3 R$ 15.800.000 / Q4 R$ 18.100.000. Crescimento anual de 44,8% em relação a 2024.",
     "receita bruta anual 2025 DRE", "Alta"),

    ("Financeiro e Contábil", "dre",
     "Qual foi o lucro líquido total em 2025?",
     "O lucro líquido consolidado de 2025 foi de R$ 25.350.000,00. O melhor trimestre foi Q4 com R$ 8.200.000 impulsionado pela expansão de contratos enterprise e redução de custos de infraestrutura OCI.",
     "lucro liquido anual 2025", "Alta"),

    ("Financeiro e Contábil", "custos",
     "Quais foram os custos com OCI Cloud em 2025?",
     "Os custos operacionais com Oracle Cloud Infrastructure (OCI) em 2025 totalizaram R$ 5.450.000,00 sendo: Q1 R$ 1.200.000 / Q2 R$ 1.350.000 / Q3 R$ 1.400.000 / Q4 R$ 1.500.000. O crescimento foi proporcional ao aumento de uso dos serviços de IA.",
     "custos oci cloud financeiro", "Alta"),

    ("Financeiro e Contábil", "despesas",
     "Qual a política de reembolso de despesas de viagem?",
     "Despesas de viagem são reembolsadas mediante aprovação prévia do gestor e apresentação de notas fiscais no sistema SAP em até 10 dias após a viagem. O limite de diária é R$ 350 para refeições e R$ 450 para hospedagem em capitais.",
     "reembolso viagem despesa politica", "Alta"),

    ("Financeiro e Contábil", "orcamento",
     "Como funciona o processo de aprovação de orçamento?",
     "Orçamentos acima de R$ 10.000 requerem aprovação da diretoria financeira. Acima de R$ 50.000 exigem aprovação do CFO. O processo é realizado via sistema de workflow SAP com prazo de resposta de 3 dias úteis.",
     "orcamento aprovacao financeiro", "Alta"),

    ("Financeiro e Contábil", "despesas_pessoal",
     "Qual o custo total com folha de pagamento em 2025?",
     "As despesas com pessoal em 2025 totalizaram R$ 19.200.000,00 sendo: Q1 R$ 4.500.000 / Q2 R$ 4.700.000 / Q3 R$ 4.900.000 / Q4 R$ 5.100.000. O crescimento reflete as contratações para expansão das equipes de IA e P&D.",
     "folha pagamento custo pessoal RH", "Alta"),

    ("Operacional", "incidente",
     "Qual o tempo máximo de resposta para incidentes críticos?",
     "Para incidentes de severidade 1 (crítico) o tempo máximo de resposta é 15 minutos. Para severidade 2 é 1 hora e severidade 3 é 4 horas. A equipe DevOps deve ser notificada no canal #ti-incidentes no Slack imediatamente.",
     "incidente critico resposta sla tempo", "Alta"),

    ("Operacional", "incidente",
     "Como reportar uma falha no servidor?",
     "Em caso de falha no servidor: 1) Notificar a equipe DevOps no canal #ti-incidentes no Slack. 2) Abrir chamado no ServiceNow com severidade adequada. 3) Seguir o Runbook de Incidentes disponível na base de conhecimento de TI.",
     "falha servidor reportar incidente", "Alta"),

    ("Operacional", "chamado",
     "Como abrir um chamado de suporte de TI?",
     "Os chamados de suporte devem ser abertos no portal ServiceNow. Inclua: descrição detalhada do problema, evidências (prints/logs) e impacto nos negócios. O SLA padrão é de 24h para chamados de baixa prioridade.",
     "chamado suporte TI servicenow", "Alta"),

    ("Operacional", "acesso",
     "Como solicitar acesso a um novo sistema?",
     "Solicitações de acesso devem ser feitas pelo gestor do colaborador no portal de Identity Management. O prazo de provisionamento é de 2 dias úteis para sistemas corporativos e 5 dias para sistemas de parceiros externos.",
     "acesso sistema solicitacao provisionamento", "Alta"),

    ("Operacional", "backup",
     "Qual a política de backup dos sistemas?",
     "Os backups são realizados diariamente às 02h com retenção de 30 dias. Backups semanais são retidos por 12 meses no OCI Object Storage. A restauração de dados deve ser solicitada via chamado de TI com SLA de 4 horas.",
     "backup politica retencao restauracao", "Alta"),

    ("Operacional", "servidor",
     "Qual o procedimento em caso de queda do servidor de produção?",
     "Protocolo de queda de servidor: 1) Notificar #ti-incidentes no Slack imediatamente. 2) Verificar status no OCI Console. 3) Ativar instância de failover em standby. 4) Notificar clientes afetados via status page. 5) Iniciar RCA em até 1h após restauração.",
     "servidor producao queda protocolo", "Alta"),

    ("Estratégico", "okrs",
     "Quais são os OKRs da empresa para 2026?",
     "Os principais OKRs de 2026 são: Objetivo 1 - Liderança em IA: ARR de R$ 50M / 150 novos clientes enterprise / NDR acima de 125%. Objetivo 2 - Excelência Operacional: 100% das cargas em OCI / latência RAG abaixo de 450ms / SLA de 99.99%.",
     "okr meta 2026 estrategia", "Alta"),

    ("Estratégico", "okrs",
     "Qual a meta de ARR para 2026?",
     "A meta de Receita Recorrente Anual (ARR) para 2026 é de R$ 50.000.000,00 (50 milhões). Isso representa um crescimento de 82% em relação ao resultado de 2025. A principal alavanca de crescimento é a expansão enterprise na América Latina.",
     "ARR meta receita 2026", "Alta"),

    ("Estratégico", "expansao",
     "Quais são os planos de expansão da empresa?",
     "Os planos de expansão para 2026 incluem: conquistar 150 novos clientes enterprise na América Latina; abrir escritórios em Buenos Aires e Cidade do México; e expandir as equipes de P&D e Engenharia de IA no primeiro semestre com foco em parcerias estratégicas.",
     "expansao plano america latina 2026", "Alta"),

    ("Estratégico", "sla",
     "Qual o SLA de disponibilidade dos sistemas de IA?",
     "A meta de SLA de disponibilidade (uptime) para todos os agentes RAG em produção é de 99.99% para 2026. Isso corresponde a no máximo 52 minutos de indisponibilidade por ano. Monitoramento 24/7 via OCI Monitoring.",
     "SLA disponibilidade uptime", "Alta"),

    ("Estratégico", "kpi",
     "Quais são os principais KPIs monitorados?",
     "Os KPIs estratégicos monitorados são: ARR / NDR (Net Dollar Retention) / Churn Rate / NPS (Net Promoter Score) / Latência média do agente RAG / SLA Uptime. Dashboard em tempo real no OCI Monitoring.",
     "KPI indicador monitoramento estrategico", "Alta"),

    ("Legal e Compliance", "lgpd",
     "Quem é o DPO responsável pela LGPD?",
     "A Encarregada de Proteção de Dados (DPO) é a Dra. Renata Vasconcelos. Contato: dpo@nexusenterprise.com.br / +55 11 3000-8800. Ela é responsável por todas as questões relacionadas ao tratamento de dados pessoais e conformidade com a LGPD.",
     "DPO LGPD responsavel privacidade", "Alta"),

    ("Legal e Compliance", "lgpd",
     "Por quanto tempo os logs de acesso ao agente de IA são retidos?",
     "Os logs de acesso ao agente de IA são retidos por 180 dias conforme o Marco Civil da Internet (Lei 12.965/2014). Após esse prazo os dados são anonimizados e arquivados. O armazenamento é realizado com criptografia AES-256 no OCI Object Storage.",
     "logs retencao 180 dias marco civil", "Alta"),

    ("Legal e Compliance", "lgpd",
     "Qual a política de retenção de dados cadastrais?",
     "Os dados cadastrais de clientes são retidos por 5 anos após o encerramento do contrato conforme a LGPD. Currículos de candidatos RH são mantidos por 12 meses com consentimento expresso. Após os prazos os dados são excluídos definitivamente.",
     "retencao dados cadastrais lgpd", "Alta"),

    ("Legal e Compliance", "privacidade",
     "Como a empresa protege os dados pessoais dos colaboradores?",
     "Os dados pessoais são protegidos por: criptografia ponta a ponta AES-256 no armazenamento OCI; acesso controlado por RBAC; auditorias de segurança semestrais; e consentimento explícito para cada tratamento de dados conforme os princípios da LGPD.",
     "protecao dados pessoais criptografia lgpd", "Alta"),

    ("Legal e Compliance", "contrato",
     "Qual o prazo de assinatura do NDA para novos fornecedores?",
     "O NDA (Non-Disclosure Agreement) deve ser assinado antes do início de qualquer prestação de serviço. O prazo para envio e devolução assinado é de 5 dias úteis. A gestão é feita pelo time Jurídico via sistema DocuSign.",
     "NDA contrato fornecedor prazo", "Alta"),

    ("Legal e Compliance", "auditoria_lgpd",
     "Com que frequência é auditada a conformidade com a LGPD?",
     "A auditoria de conformidade LGPD é realizada semestralmente pelo time de Jurídico e Compliance em conjunto com o DPO. Auditores externos certificados validam os processos anualmente. Relatórios são submetidos à ANPD quando solicitado.",
     "auditoria LGPD conformidade semestral", "Alta"),

    ("Marketing e Comercial", "precos",
     "Qual é o preço do plano Business Pro?",
     "O plano Business Pro tem preço mensal de R$ 4.990,00 e inclui: 100 usuários / 250 GB de armazenamento no OCI / suporte com SLA de 4 horas / acesso completo à plataforma de agentes RAG corporativos.",
     "Business Pro preco plano", "Alta"),

    ("Marketing e Comercial", "precos",
     "Quais são os planos disponíveis e seus preços?",
     "Os planos disponíveis são: Starter AI (R$ 1.490/mês - 25 usuários) / Business Pro (R$ 4.990/mês - 100 usuários) / Enterprise Premium (R$ 12.900/mês - ilimitado) / Custom OCI Cloud (sob consulta - customizado).",
     "planos precos starter enterprise", "Alta"),

    ("Marketing e Comercial", "precos",
     "Qual o plano mais completo disponível?",
     "O plano Enterprise Premium é o mais completo com preço de R$ 12.900,00/mês. Inclui: usuários ilimitados / 1 TB de armazenamento OCI / suporte dedicado com SLA de 1 hora / gerente de conta exclusivo / integração com sistemas legados via API.",
     "Enterprise Premium plano completo", "Alta"),

    ("Marketing e Comercial", "desconto",
     "Existe desconto para contrato anual?",
     "Sim. Contratos com pagamento anual antecipado recebem 20% de desconto sobre o valor mensal para os planos Starter e Business Pro. Para o plano Enterprise o desconto pode chegar a 30% com negociação direta com o time comercial.",
     "desconto contrato anual", "Alta"),

    ("Marketing e Comercial", "suporte",
     "Qual o SLA de suporte para clientes Enterprise?",
     "Clientes Enterprise Premium têm SLA de suporte de 1 hora para incidentes críticos com atendimento 24/7 via canal dedicado. Cada cliente Enterprise conta com um Gerente de Sucesso do Cliente (CSM) exclusivo para acompanhamento.",
     "suporte enterprise sla 1 hora", "Alta"),

    ("Dados e Sistemas", "api",
     "Qual é o endpoint principal de consulta ao agente RAG?",
     "O endpoint de consulta ao agente RAG é POST /api/v1/chat/query. O payload deve incluir os campos: query (string com a pergunta) e domain (setor do usuário). A autenticação é via Bearer Token OAuth2 / OCI IAM Token. Tempo de resposta esperado: abaixo de 500ms.",
     "endpoint api chat query", "Alta"),

    ("Dados e Sistemas", "api",
     "Como fazer upload de documentos via API?",
     "Use o endpoint POST /api/v1/documents/upload com autenticação Bearer OAuth2. O body deve ser multipart/form-data com os campos: file (binário) e domain (setor). Formatos suportados: PDF Word Excel PowerPoint Markdown CSV JSON HTML.",
     "upload api endpoint documentos", "Alta"),

    ("Dados e Sistemas", "banco",
     "Qual é o schema do banco de dados principal?",
     "O banco de dados principal usa PostgreSQL 15 hospedado no OCI Database Service. As tabelas principais são: documents (metadados) / chunks (fragmentos indexados) / audit_log (rastro de acesso RBAC) / users (colaboradores e perfis). Schema versionado via Alembic.",
     "schema banco dados postgresql", "Alta"),

    ("Dados e Sistemas", "seguranca",
     "Como é garantida a segurança dos dados no sistema?",
     "A segurança é garantida por: criptografia AES-256 em repouso e TLS 1.3 em trânsito / autenticação OAuth2 + OCI IAM / RBAC granular por setor / logs de auditoria imutáveis / pentest semestral / conformidade com ISO 27001.",
     "seguranca dados criptografia oci", "Alta"),

    ("Pesquisa e Desenvolvimento", "business_case",
     "Qual o ganho de produtividade com o agente RAG corporativo?",
     "Estudos de viabilidade demonstram ganho médio de 35% de produtividade na busca por informações internas. O tempo médio para encontrar um documento caiu de 8 minutos para 45 segundos com o agente RAG. ROI estimado em 18 meses.",
     "produtividade ganho rag business case", "Alta"),

    ("Pesquisa e Desenvolvimento", "inovacao",
     "Quais são os projetos de P&D em andamento?",
     "Os projetos ativos de P&D incluem: Agente RAG Multimodal (imagens e áudio) / Integração com OCI Generative AI (LLMs nativos) / Sistema de fine-tuning corporativo / Expansão para análise de contratos jurídicos com NLP avançado.",
     "PD projeto inovacao pesquisa", "Alta"),

    ("Pesquisa e Desenvolvimento", "roadmap",
     "Qual o roadmap de produto para 2026?",
     "O roadmap 2026 inclui: Q1 - Integração OCI Generative AI / Q2 - Agente Multimodal (PDF com imagens) / Q3 - Análise de contratos com NLP / Q4 - Fine-tuning corporativo e API pública v2. Detalhes no Confluence (acesso restrito P&D).",
     "roadmap produto 2026 pd", "Alta"),

    ("Qualidade", "auditoria",
     "Com que frequência são realizadas auditorias de TI?",
     "As auditorias internas de TI e Infraestrutura Cloud são realizadas trimestralmente. A auditoria de Segurança da Informação e LGPD é semestral. A auditoria externa de certificação ISO é anual. Os relatórios ficam disponíveis no sistema de Qualidade.",
     "auditoria TI frequencia trimestral", "Alta"),

    ("Qualidade", "iso",
     "O que é o processo de Ação Corretiva após falha em produção?",
     "Quando uma falha é identificada em produção o comitê de qualidade tem até 48 horas para publicar o Relatório de Análise de Causa Raiz (RCA). O plano de ação corretiva deve ser implementado em até 15 dias úteis com validação formal.",
     "acao corretiva RCA producao qualidade", "Alta"),

    ("Qualidade", "nao_conformidade",
     "Como registrar uma não conformidade?",
     "Não conformidades devem ser registradas no sistema de Gestão da Qualidade (ISO 9001) via portal interno. Inclua: descrição do desvio / impacto estimado / evidências / área responsável. O prazo para análise inicial é de 2 dias úteis.",
     "nao conformidade iso registro", "Alta"),

    ("Qualidade", "certificacao",
     "A empresa possui certificação ISO 9001?",
     "Sim. A empresa possui certificação ISO 9001:2015 desde 2023 com auditoria de manutenção anual pela SGS Brasil. O certificado cobre os processos de desenvolvimento de software / suporte ao cliente e operações de nuvem (OCI). Próxima auditoria: março de 2027.",
     "certificacao ISO 9001 empresa", "Alta"),

    ("Comunicação Interna", "reuniao",
     "Quando acontecem as reuniões gerais da empresa?",
     "As reuniões gerais (All-Hands) acontecem mensalmente no último dia útil do mês. Reuniões de time são semanais toda terça-feira às 09h. O canal oficial de comunicação corporativa é o Slack. Atas são publicadas no Confluence em até 24h.",
     "reuniao geral all-hands semanal", "Alta"),

    ("Comunicação Interna", "canal",
     "Qual o canal oficial de comunicação da empresa?",
     "O canal oficial de comunicação é o Slack. Os canais principais são: #geral (comunicados da diretoria) / #ti-incidentes (falhas de sistema) / #novidades-produto (lançamentos) / #rh-avisos (políticas de RH). E-mail corporativo para comunicações formais.",
     "slack canal comunicacao oficial", "Alta"),

    ("Comunicação Interna", "evento",
     "Como me informar sobre eventos corporativos?",
     "Os eventos corporativos são divulgados no canal #geral do Slack e no portal do colaborador (intranet). A agenda anual de eventos é publicada em Janeiro de cada ano pela equipe de Comunicação Interna.",
     "evento corporativo comunicacao interna", "Alta"),

    ("Comunicação Interna", "newsletter",
     "Como receber a newsletter interna da empresa?",
     "A newsletter corporativa 'Nexus Week' é enviada toda sexta-feira por e-mail para todos os colaboradores. Para se inscrever acesse o portal do colaborador ou envie e-mail para comunicacao@nexusenterprise.com.br. Edições anteriores estão no Confluence.",
     "newsletter comunicacao interna semanal", "Alta"),
]

HEADERS = ["setor", "intencao", "pergunta", "resposta", "palavras_chave", "confianca"]

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(HEADERS)
    writer.writerows(ROWS)

print(f"✅ CSV de diálogo gerado: {OUTPUT_PATH}")
print(f"   {len(ROWS)} diálogos | {len(set(r[0] for r in ROWS))} setores cobertos")
