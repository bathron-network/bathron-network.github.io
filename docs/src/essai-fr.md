# Comprendre BATHRON — un essai calme (français)

> *Version française de l'essai — English version: [Understanding BATHRON — a calm
> essay](essay.md).*

Ce texte est prévu pour être lu lentement, à voix haute si l'on veut. Il explique le
mécanisme économique et technique de BATHRON tel qu'il est envisagé aujourd'hui — en
distinguant, du début à la fin, trois choses qu'il ne faut jamais confondre : **ce qui
existe déjà dans le code**, **ce qui est un objectif de design**, et **ce qui reste une
hypothèse de marché**. Il ne contient aucune promesse, et il n'emploie jamais le mot
« trustless » sans expliquer ce qui reste à croire.

---

## 1. Ce que Bitcoin fait très bien, et où il s'arrête

Commençons par rendre à Bitcoin ce qui lui appartient.

Bitcoin est remarquable pour une chose précise : détenir et transférer du bitcoin. Une
personne possède des bitcoins parce qu'elle contrôle une clé. Elle signe une transaction,
le réseau l'enregistre, et une fois la transaction suffisamment confirmée, il devient
extraordinairement difficile de la modifier. Pas de banque qui tient un registre privé,
pas d'opérateur central qui décide des soldes : des règles publiques, vérifiables par
n'importe qui, respectées depuis plus de quinze ans.

Mais cette force ne couvre pas tous les besoins de règlement.

Un paiement ordinaire est simple : Alice envoie du bitcoin à Bob. Un **règlement
conditionnel** est autre chose : Bob ne doit recevoir l'argent que si une condition
précise est remplie, et si elle ne l'est pas avant une date donnée, Alice doit être
remboursée — automatiquement, sans dépendre de la bonne volonté de qui que ce soit.

Bitcoin sait exprimer certaines conditions simples : une signature, la révélation d'un
secret, un délai. Mais dès qu'on veut une logique commerciale complète — des conditions
composées, la vérification d'un événement, la coordination de plusieurs transactions, le
cas où une partie disparaît — le petit langage de Bitcoin ne suffit plus. Il a été
volontairement bridé, il y a longtemps, par prudence, et ce bridage est défendu par des
gens sérieux avec de bons arguments : chaque capacité ajoutée à un système qui protège
des centaines de milliards est un risque ajouté.

Des propositions pour enrichir ce langage circulent depuis des années. L'une d'elles
dispose même, au moment où ce texte est écrit, d'un calendrier d'activation *proposé* —
proposé, pas adopté ; personne ne sait si cela aboutira.

BATHRON ne part donc pas de l'idée que Bitcoin serait mauvais. Il part de l'idée inverse :
Bitcoin est une excellente couche de propriété et de transfert, et certaines opérations
conditionnelles sont difficiles à organiser directement dessus — surtout si l'on refuse
qu'un intermédiaire conserve durablement l'argent des clients.

---

## 2. Les ponts : à qui fait-on confiance, pour quoi, et combien de temps

Face à cette limite, la réponse classique consiste à sortir de Bitcoin : on immobilise du
bitcoin d'un côté, on crée une représentation de ce bitcoin sur un autre système, on y
fait ce que Bitcoin ne permet pas, puis — en théorie — on revient. Cela s'appelle un pont,
et tout pont pose une question unique : *pendant que vous êtes de l'autre côté, qui tient
vos bitcoins ?*

Un **custodian** est un gardien : une entreprise qui conserve les fonds pour le compte des
utilisateurs. Le système fonctionne tant que ce gardien reste solvable, honnête,
disponible, et autorisé à honorer les retraits.

Une **fédération** est un groupe de gardiens : plusieurs institutions doivent signer
ensemble pour déplacer les fonds. C'est mieux — une seule clé compromise ne suffit plus.
Mais le problème de fond demeure : les bitcoins existent toujours, dans une réserve
contrôlée par des acteurs identifiables. Une majorité de signataires peut les déplacer ;
une autorité peut contraindre les membres ; des clés peuvent être perdues.

Les constructions les plus récentes, dites optimistes, font encore mieux : il suffit
qu'*un seul* surveillant honnête existe pour empêcher la fraude. C'est un vrai progrès —
et il repose encore sur une cérémonie de départ honnête, des opérateurs désignés
d'avance, et des surveillants vivants et financés pendant toute la vie du pont.

Aucun de ces systèmes n'est absurde. Certains sont bien administrés et utiles. Mais il ne
faut jamais dire qu'ils sont « sans confiance ». Il faut dire précisément **à qui**
l'utilisateur fait confiance, **pour quoi**, et **pendant combien de temps**. Et dans tous
les cas, la réponse contient un gardien — parce que le bitcoin d'origine existe encore, et
que quelqu'un le tient.

---

## 3. Pourquoi le règlement exige un état interne

L'idée fondatrice de BATHRON est le règlement conditionnel sans dépositaire commun. La
chaîne peut vérifier des faits Bitcoin, mais elle ne peut pas commander une dépense
Bitcoin. Les contrats ont donc besoin d'un état interne qu'ils peuvent verrouiller et
libérer. Le mécanisme choisi pour acquérir cet état est sévère : un professionnel ne
confie pas ses bitcoins à une réserve — il les détruit.

Détruire a un sens technique précis. Il est possible d'envoyer des bitcoins vers une
condition de dépense conçue pour qu'ils soient définitivement irrécupérables. Pas une clé
perdue : une absence de clé, démontrable. Ce geste s'appelle un *burn*, et il est inscrit
pour toujours dans le registre public de Bitcoin.

En face, sur la chaîne BATHRON, chaque satoshi prouvé brûlé fait naître exactement un
satoshi d'unité comptable M0. Un pour un. Et cette création n'est pas décidée par un
guichet : la chaîne BATHRON vérifie elle-même, dans ses propres règles de consensus, que
le burn a eu lieu sur Bitcoin. **Ceci existe dans le code aujourd'hui et fonctionne sur le
réseau de test** : il n'y a eu aucune distribution initiale aux fondateurs, il n'existe
aucune récompense de bloc, et l'unique voie de création de M0 est la destruction
prouvée de bitcoin.

Ce que le burn supprime, c'est exactement la faiblesse des ponts : la réserve récupérable.
Plus de coffre à piller, plus de fédération à contraindre, plus de dépositaire à assigner,
plus de sortie à autoriser. Il n'y a rien à saisir, parce qu'il n'y a plus rien.

Ce que le burn fige, c'est l'autre face : **le chemin est à sens unique**. Aucun mécanisme,
nulle part dans le protocole, ne retransforme les unités internes en bitcoins. Celui qui
brûle acquiert un inventaire professionnel sans sortie protocolaire. Sa valeur externe
réalisable dépend de la liquidité future et peut être nulle. Si le réseau échoue, ce
capital est perdu.

Et disons ce qui reste à croire, puisque ce texte s'y est engagé : la lecture des burns
repose sur l'hypothèse que la majorité de la puissance de calcul de Bitcoin est honnête ;
la chaîne BATHRON a ses propres opérateurs, dont une majorité qualifiée doit être
honnête ; et il faut, comme toujours, faire confiance au logiciel qu'on utilise. Des
hypothèses réelles — différentes, et sans doute plus saines, que « une entreprise tient
mon argent ».

Une dernière évidence, qui commande tout le reste : **ce n'est pas l'utilisateur ordinaire
qui brûle**. Demander au grand public une action irréversible pour utiliser un service
serait une mauvaise expérience et une mauvaise répartition du risque. Celui qui brûle est
un professionnel, en connaissance de cause, comme on immobilise du capital pour ouvrir un
commerce. Nous ferons sa connaissance au chapitre six.

---

## 4. M0 et M1 : le coffre et le ticket

Deux noms techniques traversent la documentation : M0 et M1. Une image suffit.

Pensez à un vestiaire. Vous déposez un manteau ; on vous remet un ticket. Le manteau dort
dans la penderie, le ticket circule, et une règle stricte les relie : autant de tickets
que de manteaux.

**M0, c'est le manteau** : l'état comptable de base, créé à partir de burns vérifiés. Quand on veut s'en servir
pour du règlement, on la dépose dans un coffre — tenu non par une entreprise, mais par la
règle commune de la chaîne, celle que tous les nœuds font respecter ensemble.

**M1, c'est le ticket** : le reçu qui atteste qu'un montant dort au coffre, et c'est lui
qui circule et s'engage dans les contrats. La règle du vestiaire est vérifiée à chaque
bloc : le total des tickets égale exactement le total en coffre, un pour un, convertible
librement dans les deux sens. Cette égalité est un *invariant* — une propriété que le code
vérifie en permanence. **Ceci existe aujourd'hui dans le code.**

Pourquoi deux étages ? Pour séparer la réserve de la circulation : un socle rigide et
ennuyeux, une couche active et contractuelle. Et précisons ce que M1 n'est pas : ni un
jeton d'investissement, ni un titre qui rapporte. C'est un instrument de règlement, dont
la valeur, en dernier ressort, dépend du succès du système entier.

---

## 5. Le client reste en bitcoin

Voici le principe d'ergonomie qui gouverne le modèle — et c'est un **objectif de design**,
une architecture voulue et cohérente, pas encore un service en production.

Dans ce modèle, le client ordinaire vit entièrement en bitcoin. Il ne détient jamais de
M1, ne voit jamais un burn, n'apprend jamais le vocabulaire de ce texte. Son expérience
tient en une phrase, affichée avant de commencer : « vous envoyez tant de BTC ; le
bénéficiaire recevra tant, si telle condition est remplie, dans tel délai ; sinon vous
serez remboursé intégralement avant telle date ; voici les frais. » Il paie en bitcoin ;
quelqu'un, à l'autre bout, reçoit des bitcoins.

Toute la mécanique travaille en coulisse, comme les systèmes interbancaires travaillent
derrière une carte de paiement sans que personne connaisse leur nom. On peut se
représenter l'ensemble, par analogie, comme une **chambre de compensation** : une
institution discrète qui enregistre les engagements, compense les dettes croisées et fait
respecter les règles du règlement — à ceci près qu'ici, les règles ne sont pas appliquées
par une institution qui pourrait fauter, mais par le consensus d'une chaîne.

Mais si le client ne brûle rien et ne détient rien — qui fait tourner la coulisse ?

---

## 6. Clearing Provider et Liquidity Provider : qui porte le risque

Le personnage tourné vers le client est le **Clearing Provider (CP)**. Il faut d'emblée
le distinguer d'un intermédiaire de garde : un prestataire
custodial *reçoit* l'argent du client et met à jour sa base de données ; le CP, dans le
modèle visé, *route* un flux encadré par contrat, sans jamais recevoir
l'argent du client comme un dépôt libre. Il apporte la liquidité ; il ne doit pas avoir de
pouvoir arbitraire sur le résultat.

Le CP peut financer son propre inventaire ou agréger un ou plusieurs **Liquidity
Providers (LP)**. Les LP détiennent du bitcoin d'un côté et du M1 de l'autre. Pour
constituer le stock M1, un LP peut brûler des bitcoins. Ce coût d'acquisition irréversible
appartient au professionnel, pas au client.

Ses revenus, dans le modèle : un écart entre prix d'entrée et de sortie — un *spread* —,
et des frais sur les services conditionnels que le paiement simple ne sait pas rendre. Le
spread lui sert aussi de gouvernail : quand son stock de M1 baisse, il cote mieux les flux
qui le regarnissent et renchérit ceux qui le consomment ; quand c'est son stock de
bitcoins, il fait l'inverse. Son inventaire respire à travers ses prix — le métier
ordinaire des teneurs de marché.

Ses risques, dits sans fard : le capital brûlé, à amortir sur des années ; le risque de
prix sur son stock ; le risque de déséquilibre, si les flux vont durablement dans un seul
sens ; le risque de délai, quand le capital reste immobilisé dans des opérations en
cours ; et le coût d'opportunité de tout cet argent. S'il veut un jour réduire sa
position, il ne peut la revendre qu'à d'autres professionnels — s'il en existe.

Son équation est d'une simplicité brutale : il faut que les recettes dépassent les coûts,
durablement. Et il faut le dire sans détour : **personne ne sait aujourd'hui si cette
équation peut être positive.** C'est l'hypothèse de marché centrale du projet — à mesurer
avec de vrais professionnels et leurs vrais chiffres, pas à supposer.

---

## 7. Alice et Bob, pas à pas

Voici l'histoire qui justifie l'ensemble. Alice achète à Bob un objet de valeur. Ils ne se
connaissent pas. Alice refuse de payer avant de recevoir ; Bob refuse d'expédier avant
d'être payé. Le plus vieux blocage du commerce.

Déroulons la version BATHRON — en gardant à l'esprit que ce parcours *complet* est un
objectif de design : les briques existent, l'assemblage n'est pas encore un produit.

**Le devis.** Alice s'adresse au service d'un CP. On lui affiche en
clair : montant à envoyer, montant que Bob recevra, condition de libération, date limite,
frais — et la garantie recherchée : remboursement automatique si rien ne s'est passé à
l'échéance.

**Le verrouillage.** Alice envoie ses bitcoins — non dans la poche de quelqu'un, mais dans
un contrat. Dès cette seconde, cet argent n'a plus que deux avenirs possibles, inscrits
dans le contrat même : finir chez Bob si la condition est remplie, ou revenir à Alice
après l'échéance. Pas de troisième chemin ; pas de clause « à la discrétion du
prestataire ».

**La coulisse.** Le fournisseur met en place, sur BATHRON, le miroir de l'opération avec
son propre M1 : le séquestre, la condition, les délais. Alice n'en voit rien.

**Le dénouement.** Bob livre, la condition se réalise, le contrat le constate — nous
allons voir comment — et libère les fonds vers Bob, en bitcoins, par le chemin prévu. Ou
bien Bob ne livre pas, conteste, disparaît : alors personne ne décide rien ; le temps
passe, l'échéance tombe, et le remboursement d'Alice s'exécute.

À aucun moment un intermédiaire n'a détenu l'argent d'Alice avec le pouvoir d'en faire
autre chose que les deux issues prévues. Voilà le service recherché.

---

## 8. Les quatre rouages : le cadenas, le sceau, l'œil et l'horloge

Quatre mécanismes portent cette histoire.

**Le cadenas à secret — le HTLC.** Une somme est verrouillée de sorte qu'elle s'ouvre soit
avec un secret — un mot de passe cryptographique — soit, à défaut, par un remboursement
après délai. La beauté du procédé : on peut poser *le même secret* sur deux verrous, dans
deux mondes différents. Celui qui révèle le secret pour encaisser d'un côté le rend, par
là même, utilisable de l'autre. Les deux jambes du paiement — celle d'Alice qui entre,
celle de Bob qui sort — deviennent solidaires. Technique ancienne et éprouvée dans
l'écosystème Bitcoin.

**Le sceau sur les avenirs — le covenant, dont CTV.** Au moment où l'argent entre dans le
contrat, la liste exhaustive de ses sorties autorisées est scellée cryptographiquement.
« Vers Bob si condition, vers Alice sinon » — rien d'autre, jamais. C'est l'une des
capacités que Bitcoin n'a pas activées à ce jour ; sur BATHRON, elle existe et tourne,
avec une famille entière de mécanismes cousins. **Fait vérifiable sur le réseau de test.**
L'hypothèse restante : que le covenant ait été bien construit et que l'utilisateur — en
pratique, son logiciel — vérifie ce qu'il signe. Un contrat très restrictif peut être
mauvais si ses restrictions ont été mal choisies.

**L'œil sur Bitcoin — le SPV.** La chaîne BATHRON suit les en-têtes des blocs de Bitcoin
et vérifie, *dans ses règles de consensus*, qu'une transaction précise est incluse et
confirmée — chaque nœud refait la vérification, personne n'y croit sur parole. Un contrat
peut ainsi stipuler : « libère-toi quand telle transaction Bitcoin aura tant de
confirmations ». Pas d'oracle, pas de tiers qui atteste. **Cette capacité existe dans le
code aujourd'hui** — et, à notre connaissance, cette combinaison précise n'existe nulle
part ailleurs ; nous préférons que des tiers le vérifient plutôt que de le proclamer.
L'hypothèse restante : que la chaîne Bitcoin suivie soit bien la chaîne majoritaire, et
que la profondeur de confirmation choisie couvre le risque de réorganisation. Plus on
attend de confirmations, plus c'est sûr — et plus c'est lent.

**L'horloge — les timelocks.** Chaque chemin de remboursement s'ouvre à une date fixée
d'avance, et l'ordre des échéances n'est pas un détail : la fenêtre de Bob se ferme avant
que celle d'Alice ne s'ouvre, avec des marges pour les lenteurs des chaînes — sans quoi un
moment ambigu existerait où les deux chemins se chevauchent. Ajoutons l'hypothèse
opérationnelle qu'on oublie toujours : un droit de remboursement n'est utile que si le
logiciel d'Alice surveille la chaîne et publie la transaction au bon moment.

Un cadenas qui lie les jambes, un sceau qui fige les issues, un œil qui constate les
faits, une horloge qui garantit la fin de partie. Et la phrase de prudence qui doit suivre
immédiatement : la garantie globale — « Alice est réglée selon le devis ou remboursée,
dans *tous* les cas, y compris les pannes au pire moment » — est un **objectif de
sécurité**. Les flux n'ont pas été spécifiés formellement ; aucune revue externe n'a eu
lieu. Dire aujourd'hui « le fournisseur ne peut pas voler le principal » serait une
promesse, pas un fait — et nous nous l'interdisons tant que ce travail n'est pas fait.

---

## 9. L'économie du premier entrant

Une question décide de beaucoup : le premier Clearing Provider, qui sera-t-il ?

Mettons-nous à la place d'un teneur de marché neutre et rationnel. Il posera trois
questions. Combien ça rapporte ? — des spreads et des frais sur un volume qui n'existe pas
encore. Combien ça coûte ? — un capital brûlé, irrécupérable par le protocole, à amortir
sur des années. Et surtout : comment je sors ? — en revendant son M1 à d'autres
professionnels… qui n'existent pas encore ; ou en le consommant lentement dans
l'activité ; ou en le perdant si le réseau meurt. Pour le tout premier entrant, le marché
de sortie est vide par définition.

Un teneur de marché neutre, devant ce tableau, dit non — et il a raison selon ses
critères. La conclusion honnête est donc : **le premier fournisseur sera probablement un
sponsor stratégique**, pas un arbitragiste. Quelqu'un dont l'intérêt dépasse le rendement
du trimestre : un prestataire qui veut se différencier par le règlement conditionnel, une
maison de négoce qui veut son propre rail de séquestre, un acteur qui achète la thèse et
l'infrastructure en même temps. Il pourrait accepter une rentabilité faible ou nulle au
début, pour amorcer.

Et il faut en tirer la conséquence sur ce que prouve quoi : l'arrivée du premier prouvera
qu'un sponsor y croit. C'est le *deuxième*, indépendant, venu sans invitation, qui
prouvera qu'un marché existe. La nuance est importante — elle évite de s'applaudir au
mauvais moment.

---

## 10. L'inventaire honnête de ce qui n'est pas prouvé

Faisons la liste des manques, en chapitre à part entière.

**Aucun audit externe.** Le code a été relu et attaqué de façon répétée — par son équipe.
Dans le logiciel financier, l'auto-examen ne compte pas comme preuve. Un regard extérieur,
payé pour casser, est un prérequis à toute valeur réelle. Il n'a pas eu lieu.

**Une vulnérabilité connue et assumée.** Le réseau de test s'ouvre à des opérateurs
extérieurs avec un ticket d'entrée quasi gratuit ; il en découle qu'un acteur malveillant
pourrait, à peu de frais, créer quelques identités fictives et *geler la finalisation*
des blocs. Précisons ce que cela ne permet pas : ni voler, ni créer de la monnaie — les
invariants comptables tiennent quoi qu'il arrive, c'est dans le code. Un sabotage
visible, réversible par un redémarrage du réseau de test ; assumé pour la phase
d'expérimentation, à durcir avant tout réseau définitif.

**Aucun Clearing Provider réel.** Personne n'a ouvert de service réel de règlement conditionnel.
Aucune transaction de client réel n'a été routée. L'économie décrite plus haut est une
architecture qui attend son premier habitant.

**Une économie non prouvée.** Le fournisseur doit gagner assez ; le client doit accepter
le prix ; les deux en même temps. Un spread trop faible ne rémunère pas le capital ; un
spread trop élevé fait fuir le client. Il faudra mesurer, pas raisonner.

**Une protection client à spécifier et à revoir** — techniquement, et au-delà. Car la
protection cryptographique ne remplace pas la protection commerciale : que se passe-t-il
si l'objet livré n'est pas conforme ? qui définit que la condition est remplie ? qui
répond d'un bug d'interface ? existe-t-il un recours ? Le protocole peut garantir qu'un
secret a été révélé ; il ne garantit pas que la réalité commerciale correspond au secret.
Ces questions relèvent du service construit au-dessus — et elles restent ouvertes.

---

## 11. Face aux alternatives : qui gagne quoi

Un mot de loyauté concurrentielle, car rien ne décrédibilise plus vite que de prétendre
tout battre.

**Lightning** est meilleur pour le paiement simple et rapide, sans discussion. Il vise le
transfert de bitcoins par canaux préfinancés, avec ses propres hypothèses — liquidité des
canaux, disponibilité des routes, surveillance de la chaîne. BATHRON ne le concurrence pas
sur ce terrain ; son sujet commence là où il faut des conditions riches.

**Liquid** apporte des transferts rapides et confidentiels entre institutions, avec de la
liquidité réelle — au prix de son modèle : une fédération identifiée tient la garde, et la
sortie passe par ses membres. Compromis différent, pas absurdité ; il faut simplement
savoir qu'on l'a signé. BATHRON renonce au coffre récupérable ; en échange, sa liquidité
de sortie doit venir des fournisseurs et de leur inventaire.

**Un prestataire custodial** gagne en simplicité : dépôt, base de données, service client
— contre la garde de vos fonds et le pouvoir de trancher. BATHRON cherche à réduire ce
pouvoir par des transactions préengagées ; en échange, le système est techniquement plus
complexe.

**Le multisig avec arbitre et contrat juridique**, enfin, est l'alternative la plus
honnête pour le séquestre — et il faut lui reconnaître sa force propre : un arbitre humain
peut regarder des photos, lire des messages, juger si un produit était conforme. Aucun
contrat cryptographique ne fait cela. La délimitation loyale est donc celle-ci : **BATHRON
vise les conditions objectivement vérifiables** — un délai écoulé, une signature, une
transaction confirmée ; **l'arbitrage humain reste meilleur quand la condition demande une
interprétation**. Ce n'est pas une concession décorative : c'est la frontière du produit.

La vraie question n'est jamais « qui est supérieur » — c'est : quel type de confiance, et
quel type de coût, ce client-ci préfère-t-il ?

---

## 12. La vraie question de marché — et le résumé honnête

Tout ce que ce texte a décrit se suspend à une question d'une banalité désarmante :

*Combien un client réel accepterait-il de payer pour éviter la garde et l'arbitrage ?*

Mettez-vous à la place d'Alice. Pour son séquestre, elle a le choix : l'arbitre et ses
honoraires, le prestataire et ses conditions, ou ce rail nouveau. Quel écart de prix la
ferait choisir le rail ? Pour un petit paiement ordinaire, probablement aucun. Pour une
transaction importante, internationale, exposée au gel ou à la faillite d'un dépositaire —
peut-être beaucoup. Personne ne connaît ce chiffre. Il ne se calcule pas dans le code ; il
se mesure avec des clients réels, des offres réelles, des refus réels. Et il commande
tout : s'il est confortable, l'équation du fournisseur peut fermer et le système vivre ;
s'il est proche de zéro, aucune élégance technique n'y changera rien.

Résumons, une dernière fois, dans les trois registres.

**Ce qui existe.** Une chaîne fonctionne, sur un réseau de test public. Elle crée M0
exclusivement par destruction prouvée de bitcoins — sans prémine, sans récompense de bloc,
une unité par satoshi détruit. Elle vérifie elle-même, dans ses règles, l'état de
Bitcoin. Elle maintient un coffre et des reçus à parité stricte, vérifiée à chaque bloc.
Et elle fait tourner une famille de contrats aux chemins scellés que Bitcoin, à ce jour,
refuse d'activer. Tout cela est vérifiable par quiconque veut regarder.

**Ce qui est visé.** Un moteur de règlement conditionnel derrière une expérience bitcoin
banale : des clients qui paient et reçoivent du BTC sans rien voir de la machinerie ; des
fournisseurs professionnels qui portent l'inventaire, les prix et les risques ; et une
garantie centrale — réglé selon le devis, ou remboursé par l'horloge — qui gouverne chaque
contrat. Ce dessin est cohérent, écrit, et non construit : ni spécifié formellement, ni
audité, ni habité par un seul fournisseur réel.

**Ce qui est espéré, et pas encore su.** Qu'il existe des clients dont la douleur vaut un
prix ; que ce prix rémunère le capital brûlé d'un professionnel ; qu'un premier sponsor
franchisse la porte, puis qu'un deuxième vienne sans qu'on l'invite.

La proposition de BATHRON peut donc se formuler sans exagération. Il ne s'agit pas de
supprimer la confiance : il s'agit d'en **déplacer** une partie — remplacer la discrétion
d'un gardien par un burn irréversible, des preuves Bitcoin, des transactions préengagées,
des secrets et des délais. Le prix de ce déplacement est une complexité technique réelle
et un besoin vital de fournisseurs de liquidité. Ce qui reste à croire est nommé ; ce qui
reste à prouver est listé ; et ce qui donnerait tort au projet est écrit d'avance.

Le code existe. Le dessin est net. Le marché est une question posée — et la seule réponse
qui compte viendra d'audits externes, d'essais réels, et de clients réels.
