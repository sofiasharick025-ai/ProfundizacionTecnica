ancho=5;
alto=6;

if (ancho < 0 or alto < 0):

    print("No puedes ingresar numeros negativos");

else:

    area=ancho * alto;
    perimetro=2*(ancho + alto);

    print("Área: ",area);
    print("Perímetro: ",perimetro);


