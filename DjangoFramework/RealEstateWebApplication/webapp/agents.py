from django.db import models
from djongo import models


class Agents(models.Model):
    agentID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    commissionRate = models.IntegerField()
    company = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    
    @staticmethod
    def save_new_agent(id,name,commission,company):
        # Create a new Homes object with the desired values
        new_agent = Agents(
            agentID=id,
            name=name,
            commissionRate=commission,
            company=company,
        )
        # Save the new_home object to the database
        saved_agent= new_agent.save()
    

    
    