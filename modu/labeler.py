#!/usr/bin/env python

import argparse

HTML_LABELS = argparse.Namespace()
HTML_LABELS.RECORD = "record"
HTML_LABELS.NAME = "name"
HTML_LABELS.START = "start"
HTML_LABELS.END = "end"
HTML_LABELS.DURATION = "duration"
HTML_LABELS.BILLABLE = "billable"
HTML_LABELS.EMERGENCY = "emergency"
HTML_LABELS.LABEL = "label"
HTML_LABELS.NOTES = "notes"
HTML_LABELS.SUBMIT = "submit"
HTML_LABELS.INSERT = "insert"
HTML_LABELS.DROPDOWN = "dropdown"
HTML_LABELS.COMPLETE = "complete"
HTML_LABELS.EDIT = "edit"
HTML_LABELS.NEW_NOTES = "newNotes"
HTML_LABELS.COMPLETE_END_TIME = "completeEndTime"


# class that creates an object for labeling and id'ing HTML objects

class Labeler:


  def __init__(self, i=None):
    if i != None:
      self.i = int(i)
    else:
      self.i = None


  def inc(self):
    if self.i != None:
      self.i += 1

  def dec(self):
    if self.i != None:
      self.i -= 1


  #############################################
  def record(self):
    if self.i != None:
      return HTML_LABELS.RECORD + str(self.i)
    else:
      return HTML_LABELS.RECORD

  def name(self):
    if self.i != None:
      return HTML_LABELS.NAME + str(self.i)
    else:
      return HTML_LABELS.NAME

  def start(self):
    if self.i != None:
      return HTML_LABELS.START + str(self.i)
    else:
      return HTML_LABELS.START

  def end(self):
    if self.i != None:
      return HTML_LABELS.END + str(self.i)
    else:
      return HTML_LABELS.END

  def duration(self):
    if self.i != None:
      return HTML_LABELS.DURATION + str(self.i)
    else:
      return HTML_LABELS.DURATION

  def billable(self):
    if self.i != None:
      return HTML_LABELS.BILLABLE + str(self.i)
    else:
      return HTML_LABELS.BILLABLE

  def emergency(self):
    if self.i != None:
      return HTML_LABELS.EMERGENCY + str(self.i)
    else:
      return HTML_LABELS.EMERGENCY

  def label(self):
    if self.i != None:
      return HTML_LABELS.LABEL + str(self.i)
    else:
      return HTML_LABELS.LABEL

  def notes(self):
    if self.i != None:
      return HTML_LABELS.NOTES + str(self.i)
    else:
      return HTML_LABELS.NOTES

  def submit(self):
    if self.i != None:
      return HTML_LABELS.SUBMIT + str(self.i)
    else:
      return HTML_LABELS.SUBMIT

  def insert(self):
    if self.i != None:
      return HTML_LABELS.INSERT + str(self.i)
    else:
      return HTML_LABELS.INSERT

  def dropdown(self):
    if self.i != None:
      return HTML_LABELS.DROPDOWN + str(self.i)
    else:
      return HTML_LABELS.DROPDOWN

  def complete(self):
    if self.i != None:
      return HTML_LABELS.COMPLETE + str(self.i)
    else:
      return HTML_LABELS.COMPLETE

  def edit(self):
    if self.i != None:
      return HTML_LABELS.EDIT + str(self.i)
    else:
      return HTML_LABELS.EDIT

  def new_notes(self):
    if self.i != None:
      return HTML_LABELS.NEW_NOTES + str(self.i)
    else:
      return HTML_LABELS.NEW_NOTES

  def complete_end_time(self):
    if self.i != None:
      return HTML_LABELS.COMPLETE_END_TIME + str(self.i)
    else:
      return HTML_LABELS.COMPLETE_END_TIME


  #############################################

if __name__ == "__main__":
  print("Import class: from Labeler import *")
  print("Exiting...")
  exit()