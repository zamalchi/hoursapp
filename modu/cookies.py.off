#!/usr/bin/env python

import datetime

import modu.recorder as recorder

import bottle

""" DOESN'T WORK DON'T USE IT (was unable to pass bottle request and response objects to the class and back)
Works in conjunction with recorder.py
Instantiate with a bottle request and bottle response
Gets, sets, and deletes cookies:
  name, date, anchor, notes
"""
class Cookies:
  
  def __init__(self, request, response):
    self.request = request.copy()
    self.response = response.copy()
  
  # @property
  # def request(self):
  #   return self.__request
  #
  # @property
  # def response(self):
  #   return self.__response
  #
  ###############################################
  
  @property
  def name(self):
    return self.request.get_cookie("name") or ""
  
  @name.setter
  def name(self, val):
    self.response.set_cookie("name", str(val))
    return self.response

  def delete_name(self):
    self.response.delete_cookie("name")

  ###############################################
  
  @property
  def date(self):
    return recorder.validateDate(self.request.get_cookie("date") or datetime.date.today())
  
  @date.setter
  def date(self, val):
    self.response.set_cookie("date", str(recorder.validateDate(val)))

  def delete_date(self):
    self.response.delete_cookie("date")

  ###############################################
  
  @property
  def anchor(self):
    return self.request.get_cookie("anchor") or "-1"
  
  @anchor.setter
  def anchor(self, val):
    self.response.set_cookie("anchor", str(val))

  def delete_anchor(self):
    self.response.delete_cookie("anchor")

  ###############################################
  
  @property
  def notes(self):
    return self.request.get_cookie("notes") or ""
  
  @notes.setter
  def notes(self, val):
    self.response.set_cookie("notes", str(val))
  
  def delete_notes(self):
    self.response.delete_cookie("notes")
  
  ###############################################