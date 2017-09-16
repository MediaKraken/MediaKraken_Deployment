/*  cdrdao - write audio CD-Rs in disc-at-once mode
 *
 *  Copyright (C) 1998-2001  Andreas Mueller <andreas@daneb.de>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include <config.h>

#include <stdio.h>

#include "SubTrack.h"

SubTrack::SubTrack(Type t, unsigned long start, const TrackData &data) 
  : TrackData(data)
{
  type_ = t;
  start_ = start;
  next_ = pred_ = NULL;
}

SubTrack::SubTrack(Type t, const TrackData &data) 
  : TrackData(data)
{
  type_ = t;
  start_ = 0;
  next_ = pred_ = NULL;
}

SubTrack::SubTrack(const SubTrack &obj) : TrackData(obj)
{
  type_ = obj.type_;
  start_ = obj.start_;
  next_ = pred_ = NULL;
}

SubTrack::~SubTrack()
{
  next_ = pred_ = NULL;
}
