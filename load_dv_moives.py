import bioformats
import javabridge
import numpy as np

def read_dv_movie(movie_path):
    javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='512M')
    try:
        rdr = bioformats.ImageReader(movie_path)
        num_channels = rdr.rdr.getSizeC()
        num_frames = rdr.rdr.getSizeT()
        num_slices = rdr.rdr.getSizeZ()
        height = rdr.rdr.getSizeY()
        width = rdr.rdr.getSizeX()

        movie_data = np.empty((num_channels, num_frames, num_slices, height, width), dtype=np.uint16)

        for c in range(num_channels):
            for t in range(num_frames):
                for z in range(num_slices):
                    img = rdr.read(c=c, t=t, z=z, rescale=False)
                    movie_data[c, t, z] = img

    finally:
        javabridge.kill_vm()

    return movie_data

if __name__ == "__main__":
    movie_path = "/Users/haoranyue/Downloads/wetransfer_exp2022_h1299_eb3-mkate2_sir-dna_pi-eb1-gfp_set11_stlc_dmso_cell1_r3d_d3d-dv_2023-03-24_1830/exp2022_H1299_EB3-mKate2_SiR-DNA_pi-EB1-GFP_set11_STLC_CilioDi_cell1_R3D_D3D.dv"
    movie_data = read_dv_movie(movie_path)
    print(movie_data.shape)
