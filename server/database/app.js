/* jshint esversion: 8 */
/* jshint node: true */

'use strict';

const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

/* Middleware */
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

/* Load data */
const reviewsData = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
const dealershipsData = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

/* Database connection */
mongoose
  .connect('mongodb://mongo_db:27017/dealershipsDB')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

/* Models */
const Reviews = require('./review');
const Dealerships = require('./dealership');

/* Seed database */
(async function seedDatabase() {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);

    console.log('Database seeded successfully');
  } catch (error) {
    console.error('Database seeding error:', error);
  }
}());

/* Routes */

// Home
app.get('/', function (req, res) {
  res.send('Welcome to the Mongoose API');
});

// Fetch all reviews
app.get('/fetchReviews', async function (req, res) {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch reviews by dealer
app.get('/fetchReviews/dealer/:id', async function (req, res) {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async function (req, res) {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async function (req, res) {
  try {
    const documents = await Dealerships.find({ state: req.params.state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Fetch dealership by ID
app.get('/fetchDealer/:id', async function (req, res) {
  try {
    const document = await Dealerships.findOne({ id: req.params.id });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership by id' });
  }
});

// Insert review
app.post('/insert_review', async function (req, res) {
  try {
    const data = req.body;

    const lastReview = await Reviews.findOne().sort({ id: -1 });
    const newId = lastReview ? lastReview.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

/* Start server */
app.listen(port, function () {
  console.log('Server is running on http://localhost:' + port);
});
