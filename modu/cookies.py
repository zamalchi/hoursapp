#!/usr/bin/env python

import datetime

import modu.recorder as recorder

"""
Works in conjunction with recorder.py
Instantiate with a bottle request and bottle response
Gets, sets, and deletes cookies:
  name, date, anchor, notes
"""
class Cookies:
  
  def __init__(self, request, response):
    self.__request = request
    self.__response = response
  
  ###############################################
  
  @property
  def name(self):
    return self.__request.get_cookie("name") or ""
  
  @name.setter
  def name(self, val):
    self.__response.set_cookie("name", str(val))

  def delete_name(self):
    self.__response.delete_cookie("name")

  ###############################################
  
  @property
  def date(self):
    return recorder.validateDate(self.__request.get_cookie("date") or datetime.date.today())
  
  @date.setter
  def date(self, val):
    self.__response.set_cookie("date", str(recorder.validateDate(val)))

  def delete_date(self):
    self.__response.delete_cookie("date")

  ###############################################
  
  @property
  def anchor(self):
    return self.__request.get_cookie("anchor") or "-1"
  
  @anchor.setter
  def anchor(self, val):
    self.__response.set_cookie("anchor", str(val))

  def delete_anchor(self):
    self.__response.delete_cookie("anchor")

  ###############################################
  
  @property
  def notes(self):
    return self.__request.get_cookie("notes") or ""
  
  @notes.setter
  def notes(self, val):
    self.__response.set_cookie("notes", str(val))
  
  def delete_notes(self):
    self.__response.delete_cookie("notes")
  
  ###############################################