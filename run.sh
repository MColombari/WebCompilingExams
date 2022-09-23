docker run -it -p 5000:5000 -v $(pwd)/config.yaml:/app/config.yaml \
                            -v $(pwd)/log.txt:/app/log.txt \
                            -v $(pwd)/past_student_exam:/app/past_student_exam \
                            -v $(pwd)/questions:/app/questions \
                            mcolombari/final_webapp