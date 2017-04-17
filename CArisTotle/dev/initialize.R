#ziskame cestu k nacteni jiz naucene site
net.filename <- system.file("extdata", "net_set1.net", package="catest")

#zadame, ktere uzly jsou dovednostni
skill.vars <- c("S1")

#inicializuje se sit
bayes.net <- initialize.network(net.filename,skill.vars)


selection.criterion <- 1 # přepínač pro volbu otázek, v tuto chvili muze byt pouze 1

model <- bayes.net
#prida se evidence o studentovi (vek, pohlavi), ale nejspis o nem nic vedet nebudeme.
#evidence.data <- matrix(c(2,3), nrow = 1)
#colnames(evidence.data) <- c("promenna1", "promenna2")
#model <- insert.initial.evidence(clean.model, evidence.data)

no.states <- 2 #my mame binarni otazky, ale obecne byt nemusi
# odnekud musi prijit list predchozich odpovedi
# asi bych radeji oznacoval stavy 1-n, v nasem pripade 1 a 2
answered.questions <- list(list(name = "Q1", state = 1), list(name = "Q12", state = 2))

# vložit všechny známé odpovědi
for(question in answered.questions){
    a <- array(rep(0, no.states), dim = c(no.states)) # pole na odpovedi

    a[question$state] <- 1 #prepsani spravne hodnoty podle stavu


    index <- node.index(bayes.net, question$name)
    evidence <- list(a = a, i = index)

    model <- insert.evidence(model=model, evidence=evidence)
}

vars <- model@nodes@nodes.names
#nastavi model - spousti pocatecni inferenci na vsechny promenne - stejne jako radek pod tim
model <- prepare.model(model)
model <- one.dimensional.marginals(model, node.index(model,vars))
#pozor, ze je treba vlozit indexy uzlu v siti, ne jejich jmena

# konec inicializace