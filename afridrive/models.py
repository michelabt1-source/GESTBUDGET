from django.db import models

# Create your models here.
class Client(models.Model):
    idClient = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    idVehicle = models.AutoField(primary_key=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(_("Image"), upload_to=None, height_field=None, width_field=None, max_length=None)
    description = models.TextField()
    type= models.BooleanField()  # True for car, False for motorcycle
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"   

class Reservation(models.Model):
    idReservation = models.AutoField(primary_key=True)
    Demande = models.ForeignKey(Demande, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    dated = models.DateField()   
    datef = models.DateField()

   
    def __str__(self):
        return f"Reservation {self.idReservation} for {self.client.name} - {self.vehicle.make} {self.vehicle.model}"   
    
class Demande(models.Model):
    idDemande = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return f"Demande {self.idDemande} for {self.client.name} - {self.vehicle.make} {self.vehicle.model}"   
class payement(models.Model):
    idPayment = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    def __str__(self):
        return f"Payment {self.idPayment} for Reservation {self.reservation.idReservation} - Amount: {self.amount}"
        
      