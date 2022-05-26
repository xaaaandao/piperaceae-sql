# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    arquivo_entrada = open('piperaceae-original.csv')
    arquivo_saida = open('saida.csv', 'w')
    arquivo_saida.write('"seq","modified","institutionCode","collectionCode","catalogNumber","basisOfRecord","kingdom","phylum","class","order","family","genus","specificEpithet","infraspecificEpithet","scientificName","scientificNameAuthorship","identifiedBy","yearIdentified","monthIdentified","dayIdentified","typeStatus","recordedBy","recordNumber","fieldNumber","year","month","day","eventTime","continentOcean","country","stateProvince","county","locality","decimalLongitude","decimalLatitude","verbatimLongitude","verbatimLatitude","coordinatePrecision","boundingBox","minimumElevationInMeters","maximumElevationInMeters","minimumDepthInMeters","maximumDepthInMeters","sex","preparationType","individualCount","previousCatalogNumber","relationshipType","relatedCatalogItem","occurrenceRemarks","barcode","imagecode","geoFlag"')

    for linhas in arquivo_entrada.readlines():
        # print(linhas)
        # if linhas.lower() in 'brazil' and linhas.lower() in 'paraná' and linhas.lower() in 'brasil':
        if 'paran' in linhas.lower() or 'pr' in linhas.lower()\
            or 'sc' in linhas.lower() or 'santa catarina' in linhas.lower()\
                or 'rs' in linhas.lower() or 'rio grande do sul' in linhas.lower():
            # print('a')
                    arquivo_saida.write(linhas)

    arquivo_entrada.close()
    arquivo_saida.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
