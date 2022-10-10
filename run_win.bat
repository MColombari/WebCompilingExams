docker run -p 5000:5000 -v %cd%/config.yaml:/app/config.yaml ^
                        -v %cd%/exam:/app/exam ^
                        -v %cd%/questions:/app/questions ^
                        mcolombari/final_webapp