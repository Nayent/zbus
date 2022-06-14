de_para = {
    100: {
        'name': 'Marimbondo',
        'voltage': 500,
        'n_bar': 1
    },
    101: {
        'name': 'Araraquara',
        'voltage': 500,
        'n_bar': 2
    },
    102: {
        'name': 'Poços de Caldas',
        'voltage': 500,
        'n_bar': 3
    },
    103: {
        'name': 'Campinas',
        'voltage': 500,
        'n_bar': 4
    },
    104: {
        'name': 'Cachoeira Paulista',
        'voltage': 500,
        'n_bar': 31
    },
    122: {
        'name': 'Ibiúna',
        'voltage': 500,
        'n_bar': 5
    },
    210: {
        'name': 'Itumbiara',
        'voltage': 500,
        'n_bar': 6
    },
    233: {
        'name': 'Samambaia',
        'voltage': 500,
        'n_bar': 7
    },
    320: {
        'name': 'Emborcação',
        'voltage': 500,
        'n_bar': 8
    },
    325: {
        'name': 'Jaguara',
        'voltage': 500,
        'n_bar': 9
    },
    360: {
        'name': 'Nova Ponte',
        'voltage': 500,
        'n_bar': 10
    },
    370: {
        'name': 'São Simão',
        'voltage': 500,
        'n_bar': 11
    },
    535: {
        'name': 'Água Vermelha',
        'voltage': 500,
        'n_bar': 12
    },
    824: {
        'name': 'Gov. Bento.Munhoz',
        'voltage': 500,
        'n_bar': 13
    },
    834: {
        'name': 'Gov. Bento.Munhoz',
        'voltage': 500,
        'n_bar': 33
    },
    839: {
        'name': 'Cascavel',
        'voltage': 230,
        'n_bar': 14
    },
    856: {
        'name': 'Segredo',
        'voltage': 500,
        'n_bar': 15
    },
    895: {
        'name': 'Bateias',
        'voltage': 500,
        'n_bar': 16
    },
    896: {
        'name': 'Caqscavel do Oeste',
        'voltage': 500,
        'n_bar': 17
    },
    897: {
        'name': 'Salto Caxias',
        'voltage': 500,
        'n_bar': 18
    },
    898: {
        'name': 'Foz do Chopin',
        'voltage': 230,
        'n_bar': 19
    },
    933: {
        'name': 'Areia',
        'voltage': 500,
        'n_bar': 20
    },
    934: {
        'name': 'Areia',
        'voltage': 500,
        'n_bar': 32
    },
    938: {
        'name': 'Blumenau',
        'voltage': 500,
        'n_bar': 21
    },
    939: {
        'name': 'Blumenau',
        'voltage': 230,
        'n_bar': 36
    },
    955: {
        'name': 'Campos Novos',
        'voltage': 500,
        'n_bar': 22
    },
    959: {
        'name': 'Curitiba',
        'voltage': 500,
        'n_bar': 23
    },
    960: {
        'name': 'Curitiba',
        'voltage': 230,
        'n_bar': 37
    },
    964: {
        'name': 'Caxias',
        'voltage': 500,
        'n_bar': 24
    },
    976: {
        'name': 'Gravataí',
        'voltage': 500,
        'n_bar': 25
    },
    995: {
        'name': 'Itá',
        'voltage': 500,
        'n_bar': 26
    },
    1015: {
        'name': 'Joinville',
        'voltage': 230,
        'n_bar': 35
    },
    1030: {
        'name': 'Machadinho',
        'voltage': 500,
        'n_bar': 27
    },
    1047: {
        'name': 'Salto Osório',
        'voltage': 230,
        'n_bar': 28
    },
    1060: {
        'name': 'Salto Santiago',
        'voltage': 500,
        'n_bar': 29
    },
    1503: {
        'name': 'Itajubá',
        'voltage': 500,
        'n_bar': 30
    },
    2458: {
        'name': 'Cascavel-Oeste',
        'voltage': 230,
        'n_bar': 34
    }
}

index_name = {}
for key, item in de_para.items():
    index_name[item['n_bar'] - 1] = f'{item["name"]} ({key})'