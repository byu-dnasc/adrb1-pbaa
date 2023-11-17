import os

import fromfile

def main():
    # make sure the fastq directory exists
    os.makedirs('fastq', exist_ok=True)
 
    while True:
        try:
            input_path = input('Enter path to a BAM or XML file to be converted to FASTQ (or press ctrl-C to exit): ')

            # check that input_path is a bam or xml file
            if not input_path.endswith('.bam') and not input_path.endswith('.xml'):
                print('Path must be a bam or xml file')
                continue

            # make sure the file exists
            if not os.path.isfile(input_path):
                print('bam/xml file not found at ' + input_path)
                continue

            # get a name for the fastq file
            fastq_name = ''
            while fastq_name == '':
                fastq_name = input('Enter the name of the sample this file represents: ')

            try:
                fromfile.get_fastq(input_path, fastq_name)
            except:
                print('Error getting fastq file. Try again.')
                continue
            print('Successfully created fastq file: ' + fastq_name + '.fastq')
        except KeyboardInterrupt:
            print()
            exit()


if __name__ == '__main__':
    main()