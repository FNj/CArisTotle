library(catest)

#ziskame cestu k nacteni jiz naucene site
net.filename <- system.file("extdata", "net_set1.net", package="catest")

#zadame, ktere uzly jsou dovednostni
skill.vars <- c("S1")

#inicializuje se sit
# od zadavatele data.string,skill.vars
data.string <- readLines(net.filename)
model <- initialize.network(data.string,skill.vars,is.file = FALSE)
qe <- get.questions(model)
sk <- get.skills(model)
nl <- model@nodes[qe]
vv <- 1:length(nl@nodes)
for(node in 1:length(nl@nodes)){
    nl@nodes[[node]]@name
    vv[node] <- nl@nodes[[node]]@number.of.states
}
#bayes.net <- initialize.network(net.filename,skill.vars)


selection.criterion <- 1 # přepínač pro volbu otázek, v tuto chvili muze byt pouze 1

#model <- bayes.net
#prida se evidence o studentovi (vek, pohlavi), ale nejspis o nem nic vedet nebudeme.
#evidence.data <- matrix(c(2,3), nrow = 1)
#colnames(evidence.data) <- c("promenna1", "promenna2")
#model <- insert.initial.evidence(clean.model, evidence.data)

#no.states <- 2 #my mame binarni otazky, ale obecne byt nemusi
# odnekud musi prijit list predchozich odpovedi
# asi bych radeji oznacoval stavy 1-n, v nasem pripade 1 a 2

#answered.questions <- list("Q56" = 1, "Q1" = 2)
# answered.questions <- c("Q56", "Q1")
# answered.states <- c(1, 2)
# model <- insert.evidence(model=model, evidence=answered.questions, state = answered.states)

#answered.questions <- list(list(name = "Q56", state = 2))
# vložit všechny známé odpovědi
# for(question in answered.questions){
#   a <- array(rep(0, no.states), dim = c(no.states)) # pole na odpovedi
#
#   a[question$state] <- 1 #prepsani spravne hodnoty podle stavu
#
#
#   index <- node.index(bayes.net, question$name)
#   evidence <- list(a = a, i = index)
#
#   model <- insert.evidence(model=model, evidence=evidence)
# }

#vars <- model@nodes@nodes.names
#nastavi model - spousti pocatecni inferenci na vsechny promenne - stejne jako radek pod tim
#model <- prepare.model(model)
#model <- one.dimensional.marginals(model, node.index(model,vars))
#pozor, ze je treba vlozit indexy uzlu v siti, ne jejich jmena - uz jdou i jmena

# konec inicializace

# získat otázku k zodpovězení


#selection.criterion muze zatim byt stale 1

# questions obsahuje vsechny mozne otazky (vektor s indexy, nebo jmeny)
# question list obsahuje otazky, ktere se maji polozit
# jde o to, ze zde muzou byt napr. dvojice Nodu, ktere jsou v seznamu questions, protoze se maji polozit dohromady
# pokud takova situace neni (a v nasem pripade nejspis nebude) je mozne tento parametr vynechat a pak se berou vsechny otazky
# z questions zvlast. questions by tedy musely obsahovat pouze dosud nepolozene otazky. Na druhou stranu lze i questions nechat
# nemenne a menit jen question.list (neco jako question.list = setdiff(questions, answered.questions))
questions <- qe
question.list <- list("Q2", "Q3", c("Q4","Q5"))
question.list <- qe
pick <- pick.question(model, questions, selection.criterion = 1, question.list)

q_to_ask <- question.list[[pick$question]]
q_to_ask
# navratova hodnota je trosku komplexnejsi opet kvuli moznosti polozeni svazanych otazek. viz napoveda return:
# A list containing the selected question from \code{question.list}. This list contains
#  \code{$question} which is the index of the selected question in the \code{question.list} or the position
#   of the question node in \code{questions} if \code{question.list} was empty. The field \code{$states} contains
#    all possible states combinations of the selection (all posible states of one variable if the selection is
#     singleton). The field \code{$a} then contain prepared arrays for corresponding states (results after asking
#      the question).

# pole $a a $states je pro vas zrejme celkem nezajmave (jsou to predpriravena pole k vlozeni evidence - stejna jako ta pri
# vkladani z answered.questions). Pozor na situace, kde odpoved zahrnuje vice uzlu (svazane otazky). Tudiz je mozne, ze jedine
# zajimave je $question, coz je index moznosti z question.list

# položit otázku a získat odpověď a zkontrolovat

# pokud je dosaženo ukončovacího kritéria, ukončit test (buďto čas nebo počet otázek)

# získat výsledky

model <- one.dimensional.marginals(model, node.index(model, c(skill.vars, "Q1")))
model@marginals
model@marginals[[1]]@a