docker run -it -p 5000:5000 -v $(pwd)/config.yaml:/app/config.yaml \
                            -v $(pwd)/log.txt:/app/log.txt \
                            -v $(pwd)/exam:/app/exam \
                            -v $(pwd)/questions:/app/questions \
                            mcolombari/final_webapp