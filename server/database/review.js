/* jshint esversion: 6 */
/* jshint node: true */

'use strict';

const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const ReviewSchema = new Schema(
  {
    id: {
      type: Number,
      required: true,
      index: true
    },
    name: {
      type: String,
      required: true,
      trim: true
    },
    dealership: {
      type: Number,
      required: true,
      index: true
    },
    review: {
      type: String,
      required: true,
      trim: true
    },
    purchase: {
      type: Boolean,
      required: true
    },
    purchase_date: {
      type: String,
      required: true
    },
    car_make: {
      type: String,
      required: true,
      trim: true
    },
    car_model: {
      type: String,
      required: true,
      trim: true
    },
    car_year: {
      type: Number,
      required: true
    }
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model('Review', ReviewSchema);
