#"""
#Pre-QC,Assemble,Post-QC,Annotate RNA reads
#"""

import subprocess
from pathlib import Path

from latch import small_task, large_task, workflow
from latch.types import LatchFile, LatchDir

@small_task
def preqc_task(read1: LatchFile, read2: LatchFile, output_dir: LatchDir,) -> (LatchFile, LatchFile, LatchDir):

    qc_read1 = Path("qc_read1.fq.gz").resolve() 
    qc_read2 = Path("qc_read2.fq.gz").resolve()
    local_output_dir = "/root/fastp_output/"

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

    return (LatchFile(str(qc_read1), f"latch:///{output_dir}/qc_read1.fq.gz"), LatchFile(str(qc_read2), f"latch:///{output_dir}/qc_read2.fq.gz"), LatchDir(str(local_output_dir), output_dir.remote_path))
    

@large_task
def assemble_task(qc_read1: LatchFile, qc_read2: LatchFile, output_dir: LatchDir) -> (LatchFile, LatchDir):
# ()

    transcripts = Path(f"trinity_output/Trinity.fasta").resolve()
    local_output_dir =  "/root/assemble_output/"

    _trinity_cmd = [
        "Trinity",
        "--seqType",
        "fq",
        "--left",
        qc_read1.local_path,
        "--right",
        qc_read2.local_path,
        "--max_memory",
        "1000G",
        "--output",
        "trinity_output",
        "--no_bowtie",
    ]

    subprocess.run(_trinity_cmd)

    return (LatchFile(str(transcripts), f"latch:///{output_dir}/trinity_output/Trinity.fasta"), LatchDir(str(local_output_dir), output_dir.remote_path)) 


@workflow
def rna_denovo_assemble(read1: LatchFile, read2: LatchFile, output_dir: LatchDir) -> (LatchFile, LatchDir):
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
            
        output_dir:
          The directory where results will go.
          
          __metadata__:
            display_name: Output Directory
    """
    qc_read1, qc_read2, local_output_dir = preqc_task(read1=read1, read2=read2, output_dir=output_dir)
    transcripts, local_output_dir = assemble_task(qc_read1=qc_read1, qc_read2=qc_read2, output_dir=output_dir)
   # return postqc_task(transcripts=transcripts)
    return (transcripts, local_output_dir)