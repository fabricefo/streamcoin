### Streamlit and FastAPI

To run the example in a machine running Docker and docker compose, run:

    docker compose build
    docker compose up

To visit the FastAPI documentation of the resulting service, visit http://localhost:8502/docs with a web browser.  
To visit the streamlit UI, visit http://localhost:8501.

#### Database

CREATE TABLE public.portfolio (
	cryptoid varchar NULL,
	cryptoname text NULL,
	coingeckoid varchar NULL,
	lastprice numeric NULL,
	alert1 numeric NULL,
	alert2 numeric NULL,
	alert3 numeric NULL,
	amount numeric NULL,
	total numeric NULL
);

INSERT INTO public.portfolio
(cryptoid, cryptoname, coingeckoid, lastprice, alert1, alert2, alert3, amount, total)
VALUES(1, 'Bitcoin', 'bitcoin', 112000, 125000, 145000, 175000, 0.01, 1000);
INSERT INTO public.portfolio
(cryptoid, cryptoname, coingeckoid, lastprice, alert1, alert2, alert3, amount, total)
VALUES(2, 'Ethereum', 'ethereum', 4100, 3900, 4900, 5900, 5.63, 1000);
INSERT INTO public.portfolio
(cryptoid, cryptoname, coingeckoid, lastprice, alert1, alert2, alert3, amount, total)
VALUES(3, 'Dogecoin', 'dogecoin', 0.19, 0.38, 0.78, 0.98, 75000, 1000);


