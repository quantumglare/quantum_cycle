# quantumglare

This repo contains the code used for the article "Graph Partitioning into Hamiltonian Subgraphs on a Quantum Annealer", by Eugenio Cocchi, Edoardo Tignone and Davide Vodola. 


## How to use the code
### To set up the environment
1. Create an account on [D-Wave Leap](https://cloud.dwavesys.com/leap/signup/)

2. Duplicate the `.env.sample` file to a `.env` file and set the environment variable ```DWAVE_API_TOKEN``` to your D-Wave Leap token

3. Download [Docker](https://www.docker.com/get-started)

4. Build the image

    ```docker-compose build quantumglare```

5. Run the image as a local container (and leave it running)

    ```docker-compose up -d```
 
### To reproduce\* the results of the article
6. Generate the raw data

    ```docker-compose exec quantumglare python3 quantumglare/results/generate_raw_data.py```

7. Process the data generated at previous step

    ```docker-compose exec quantumglare python3  quantumglare/results/process_raw_data.py```
    

8. Use the processed data to generate figure 3 of the article

    ```docker-compose exec quantumglare python3  quantumglare/results/generate_figure_3.py```

9. Use the processed data to generate figure 4 of the article

    ```docker-compose exec quantumglare python3  quantumglare/results/generate_figure_4.py```
    

\* To use 50 seeds as in the article, you will need to modify the line
`seeds_embedding = list(range(0, 2))` in `quantumglare/results/generate_raw_data.py` to a list of 50 elements. However, you will need more than 60 seconds of time on D-Wave Leap in order to generate all the data. Also, note that there is some intrinsic randomness in quantum physics and therefore the output of the quantum annealer is not expected to be exactly the same every time the same experiment is run on it. However, one should obtain the same results within the errors.