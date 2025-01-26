from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.donation_platform

class Donor:
    @staticmethod
    def create_donor(data):
        donor = db.donors.insert_one(data)
        return donor.inserted_id

    @staticmethod
    def get_donors():
        return db.donors.find()

    @staticmethod
    def get_donor_by_id(donor_id):
        return db.donors.find_one({"_id": ObjectId(donor_id)})

class Volunteer:
    @staticmethod
    def create_volunteer(data):
        volunteer = db.volunteers.insert_one(data)
        return volunteer.inserted_id

    @staticmethod
    def get_volunteers():
        return db.volunteers.find()

    @staticmethod
    def get_volunteer_by_id(volunteer_id):
        return db.volunteers.find_one({"_id": ObjectId(volunteer_id)})

class Donation:
    @staticmethod
    def create_donation(data):
        donation = db.donations.insert_one(data)
        return donation.inserted_id

    @staticmethod
    def get_donations():
        return db.donations.find()

    @staticmethod
    def get_donation_by_id(donation_id):
        return db.donations.find_one({"_id": ObjectId(donation_id)})
