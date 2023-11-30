import subprocess as sub
import os
import sys
import utilitaires as util

EXECUTABLE = "DEVOIR_Exec"
FICHIERS_CODE_ETUD = ['main.cpp']
FICHIERS_TEST_ETUD = ['test3', 'test4']
FICHIERS_TEST_PROF = ['test1', 'test2', 'testProf1', 'testProf2']
FICHIERS_TEST = FICHIERS_TEST_ETUD + FICHIERS_TEST_PROF
FICHIERS_REQUIS = ['jeuxDeTest.pdf'] + FICHIERS_CODE_ETUD + FICHIERS_TEST_ETUD
FICHIERS_CODE = FICHIERS_CODE_ETUD

# ====================================================
# |   script principal                               |
# ====================================================

def execute_train(cipEtd):
    with open(cipEtd + '-output.txt', 'w+') as outputFile:
        try:
            #ETAPE 1 Valider que les fichiers requis sont presents et au bon endroit
            if util.valider_fichiers_requis(FICHIERS_REQUIS, fichierOutput=outputFile, visibleEtd=True):

                #ETAPE 2 Compiler les fichiers C++
                try:
                    util.compile_cpp(execName=EXECUTABLE, sourceFiles=FICHIERS_CODE, logFile=outputFile, std=util.CPP_17, encoding=util.ENCODAGE_UTF8, visibleEtd=True)
                except sub.CalledProcessError as e:
                    return
                nbErreurs = 0

                #ETAPE 3
                for test in FICHIERS_TEST:
                    try:
                        resultat = util.execute_test(executable=EXECUTABLE, args='', input=test, encoding=util.ENCODAGE_UTF8)
                        util.log(resultat, outputFile, True)
                    except sub.CalledProcessError as e:
                        resultat = e.output.decode(util.ENCODAGE_UTF8)
                        nbErreurs += 1

        except Exception as UE:
            util.log(str(UE), outputFile, False)
            util.log("Impossible de continuer l'exécution...", outputFile, True)

        util.log(util.create_header('Execution terminée.', '*'), outputFile, True)

# PREPARER SORTIE du TRAIN pour un utilisateur
if __name__ == "__main__":
    cip = sys.argv[1]

    try:
        execute_train(cipEtd=cip)
    except Exception as exception:
        print('Erreur : ' + str(exception))
    sys.exit(0)
