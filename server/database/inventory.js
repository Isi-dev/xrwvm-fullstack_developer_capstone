/* jshint esversion: 6 */
/* jshint node: true */

'use strict';

const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const CarSchema = new Schema(
  {
    dealer_id: {
      type: Number,
      required: true
    },
    make: {
      type: String,
      required: true,
      trim: true
    },
    model: {
      type: String,
      required: true,
      trim: true
    },
    bodyType: {
      type: String,
      required: true,
      trim: true
    },
    year: {
      type: Number,
      required: true,
      min: 1886 // first automobile year
    },
    mileage: {
      type: Number,
      required: true,
      min: 0
    }
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model('Car', CarSchema);
