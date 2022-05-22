#"""
#Pre-QC,Assemble,Post-QC,Annotate RNA reads
#"""

import subprocess
from pathlib import Path

from latch import small_task, large_task, workflow
from latch.types import LatchFile, LatchDir


#@small_task
#def getseq_task(SRR: str) -> (LatchFile, LatchFile):

    # A reference to our output.
 #   read1 = Path("read1.fq.gz").resolve()
  #  read2 = Path("read2.fq.gz").resolve()

   # _sra-tools1_cmd = [
    #    "sra-tools",
     #   "prefetch",
      #  SRR,
    #]
    
     #_sra-tools2_cmd = [
      #  "sra-tools",
       # "fasterq",
       # SRR,
        #"--split_files",
    #]

    #subprocess.run(_sra-tools1_cmd)
    #subprocess.run(_sra-tools2_cmd)

    #return LatchFile(read1, "latch:///read1.fq.gz")
    #return LatchFile(read2, "latch:///read2.fq.gz")


@small_task
def preqc_task(read1: LatchFile, read2: LatchFile) -> (LatchFile, LatchFile):

    qc_read1 = Path("qc_read1.fq.gz").resolve()
    qc_read2 = Path("qc_read2.fq.gz").resolve()

    _fastp_cmd = [
        "fastp",
        "--in1",
        read1.local_path,
       "--in2",
        read2.local_path,
       "--out1",
        str(qc_read1),
        "--out2",
        str(qc_read2),
    ]

    subprocess.run(_fastp_cmd)

    return (LatchFile(str(qc_read1), "latch:///qc_read1.fq.gz"), LatchFile(str(qc_read2), "latch:///qc_read2.fq.gz"))
    
@large_task
def assemble_task(qc_read1: LatchFile, qc_read2: LatchFile) -> LatchFile:
# ()

    transcripts = Path("Trinity.fasta").resolve()

    _trinity_cmd = [
        "Trinity",
        "--seqType",
        "fq",
        "--left",
        "latch:///qc_read1.fq.gz",
        "--right",
        "latch:///qc_read2.fq.gz",
        "--max_memory",
        "1000G",
    ]

    subprocess.run(_trinity_cmd)

    return LatchFile(str(transcripts), "latch:///Trinity.fasta")


#@large_task
#def postqc_task(transcripts: LatchFile) -> LatchFile:

 #   postqc_report = Path("transrate_results/transrate.csv").resolve()

  #  _transrate_cmd = [
  #      "transrate",
   #     "--assembly",
   #     transcripts.local_path,
   #     "--left",
   #     qcread1.local_path,
   #     "--right",
    #    qc_read2.local_path,
    #]

    #subprocess.run(_transrate_cmd)

    #return LatchFile(postqc_report, "latch:///transrate.csv")
    
#@large_task
#def getorf_task(transcripts: LatchFile):

 #  _transdecoder1_cmd = [
  #     "Transdecoder.LongOrfs",
   #    "-t",
    #   transcripts.local_path
   #]

   #subprocess.run(_transdecoder1_cmd)
    
#@large_task
#def getcds_task(transcripts: LatchFile) -> LatchFile:

 #  pep = Path("Trinity.Fasta.transdecoder.pep").resolve()

  # _transdecoder2_cmd = [
   #    "Transdecoder.Predict",
    #   "-t",
     #  transcripts.local_path
 # ]

  # subprocess.run(_transdecoder2_cmd)

   #return LatchFile(pep, "latch:///Trinity.Fasta.transdecoder.pep")

#@medium_task
#def annotate_task(transcripts: LatchFile) -> LatchDir:

	#resultsdb = Path("Trinotate.sqlite").resolve() 
	#uniprot = Path("uniprot_sprot.pep").resolve() 
	#pfam =  Path("Pfam-A.hmm.gz").resolve()  
	#blastdb = 

#_build1_cmd = ["Build_Trinotate_Boilerplate_SQLite_db.pl", "Trinotate"]
#_build2_cmd = ["makeblastdb", "-in", "uniprot_sprot.pep", "-dbtype", "prot"]
#_build3_cmd = ["gunzip", "Pfam-A.hmm.gz"]
#_build4_cmd = ["hmmpress", "Pfam-A.hmm"]
#_build5_cmd = ["blastp", "-query", "transdecoder.pep", "-db", "uniprot_sprot.pep", "-num_threads", "8", "-max_target_seqs", "1", "-outfmt", "6", "-evalue", "1e-3", ">", "blastp.outfmt6"]
#_build6_cmd = ["hmmscan", "--cpu", "12", "--domtblout", "TrinotatePFAM.out", "Pfam-A.hmm", "transdecoder.pep", ">", "pfam.log"]	

   # subprocess.run(_build1_cmd)
   # subprocess.run(_build2_cmd)
   # subprocess.run(_build3_cmd)
    #subprocess.run(_build4_cmd)
    #subprocess.run(_build5_cmd)
    #subprocess.run(_build6_cmd)
    
#@medium_task
#def results_task(transcripts: LatchFile) -> LatchDir:

#_report1_cmd = ["get_Trinity_gene_to_trans_map.pl", "Trinity.fasta", ">",  "Trinity.fasta.gene_trans_map"]
#_report2_cmd = ["Trinotate", "Trinotate.sqlite", "init", "--gene_trans_map", "Trinity.fasta.gene_trans_map", "--transcript_fasta", "Trinity.fasta", "--transdecoder_pep", "transdecoder.pep"]
#_report3_cmd = ["Trinotate", "Trinotate.sqlite", "LOAD_swissprot_blastp", "blastp.outfmt6"]	
#_report4_cmd = ["Trinotate", "Trinotate.sqlite", "LOAD_pfam", "TrinotatePFAM.out"]
#_report5_cmd = ["Trinotate", "Trinotate.sqlite", "report", ">", "trinotate_annotation_report.xls"]

    #subprocess.run(_report1_cmd)
    #subprocess.run(_report2_cmd)
    #subprocess.run(_report3_cmd)
    #subprocess.run(_report4_cmd)
    #subprocess.run(_report5_cmd)
    
@workflow
def assemble_annotate(read1: LatchFile, read2: LatchFile) -> (LatchFile, LatchFile, LatchFile):
    """

    # RNA De Novo Assembly
    
    * This workflow takes paired end transcriptome fastq files and runs pre-assembly QC with Fastp, assembly with Trinity, post-assembly QC with transrate, and annotation with Trinotate

    __metadata__:
        display_name: Assemble and Annotate Transcriptome FastQ Files
        author:
            name: Corey Howe
            email: 	
            github: 
        repository: test
        license:
            id: MIT

    Args:

        read1:
          Paired-end read 1 file to be assembled.

          __metadata__:
            display_name: Read1

        read2:
          Paired-end read 2 file to be assembled.

          __metadata__:
            display_name: Read2
    """
    qc_read1, qc_read2 = preqc_task(read1=read1, read2=read2)
    transcripts = assemble_task(qc_read1=qc_read1, qc_read2=qc_read2)
   # return postqc_task(transcripts=transcripts)
    return (qc_read1, qc_read2, transcripts)