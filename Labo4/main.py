import hashlib
import random
import string
import datetime
import copy
import azure.functions as func
import tempfile
import pathlib
import requests
import base64
import json
from logFile import log
import os
import logging
import sys
import time
from typing import Optional


def main(req: func.HttpRequest) -> func.HttpResponse:
    log('Python HTTP trigger function processed a request.')

    #contact_id: Optional[str] = None

    try:
        req_body = req.get_json()
        log(f"{req_body}")
    except ValueError:
        pass

    hash()
    return func.HttpResponse(json.dumps({}))

def chaine_aleatoire_hex(n_car):
    caracteres = string.hexdigits
    chaine = ''.join(random.choice(caracteres) for i in range(n_car))
    return chaine


def gen_all_hex(n_car):
    i = 0
    array = []
    while i < 16 ** n_car:
        array.append(('{:0'+ str(n_car) + 'X}').format(i))
        i += 1
    return array


def hash():
    message = "Bonjour, monde !"

    log(
        "\n-----------------\npreuve de travail par recherche de collisions (suite de zéros en tête de l'empreinte) pour l'algorithme SHA-1")
    log('pour la chaine : "' + message + '"')
    log("-----------------\n")

    # effectuer la recherche pour plusieurs longueurs de collisions
    for longueur in range(1, 7):

        # initialisation de la recherche
        fini = False
        essai = 0
        dt1 = datetime.datetime.now()
        log("recherche d'une collision de longueur " + str(longueur) + ", moment de début = " + str(dt1))

        temparray = gen_all_hex(longueur)
        i = 0
        # lancer la recherche
        while (not fini and i < len(temparray)):

            # où est-on rendu ?
            essai = essai + 1
            if essai % 100000 == 0:
                log("recherche en cours, essai #" + str(essai))

            # construire la chaîne combinée du message et de la chaîne candidate
            chaine_candidate = temparray[i]
            chaine_combinee = message + chaine_candidate

            # calculer l'empreinte
            empreinte = hashlib.sha1(bytes(chaine_combinee, 'ASCII')).hexdigest()

            # vérifier si on a une collision, et si oui afficher les informations pertinentes
            if empreinte[0:longueur] == '0' * longueur:
                fini = True

            i+=1

        if fini == True:
            dt2 = datetime.datetime.now()
            log(dt2 - dt1)
            log("Succès avec l'essai #" + str(essai) + " après un temps de " + str(dt2 - dt1))
            log("La chaîne combinée est : " + chaine_combinee)
            log("L'empreinte est : " + empreinte)
            log("Il est : " + str(dt2))
            log('-----------------')


if __name__ == '__main__':
    request: func.HttpRequest = func.HttpRequest(
        "GET",
        "https://sf-releve-assurance.azurewebsites.net/api/sf_releve_assurance?code=VjQiwMIVtqahlukqvpfM6md5g3Qjka6hmReNUteFvzrn1JarEtlC6w==",
        body=json.dumps({"isProduction": True, "contactId": "0033i00000RbtTgAAJ"}).encode('utf-8')
    )
    main(request)