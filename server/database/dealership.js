/* jshint esversion: 6 */
/* jshint node: true */

'use strict';

const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const DealershipSchema = new Schema(
  {
    id: {
      type: Number,
      required: true,
      index: true
    },
    city: {
      type: String,
      required: true,
      trim: true
    },
    state: {
      type: String,
      required: true,
      trim: true
    },
    address: {
      type: String,
      required: true,
      trim: true
    },
    zip: {
      type: String,
      required: true,
      trim: true
    },
    lat: {
      type: String,
      required: true
    },
    long: {
      type: String,
      required: true
    },
    short_name: {
      type: String,
      trim: true
    },
    full_name: {
      type: String,
      required: true,
      trim: true
    }
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model('Dealership', DealershipSchema);
