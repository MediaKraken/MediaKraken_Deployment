/*
 * serialize.h
 *
 *  Copyright (C) Georg Martius - January 2013
 *   georg dot martius at web dot de
 *
 *  This file is part of vid.stab video stabilization library
 *
 *  vid.stab is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License,
 *  as published by the Free Software Foundation; either version 2, or
 *  (at your option) any later version.
 *
 *  vid.stab is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with GNU Make; see the file COPYING.  If not, write to
 *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 */

#ifndef __SERIALIZE_H
#define __SERIALIZE_H

#include "transformtype.h"
#include "motiondetect.h"
#include "transform.h"


/// Vector of LocalMotions
typedef VSVector VSManyLocalMotions;
/// helper macro to access a localmotions vector in the VSVector of all Frames
#define VSMLMGet(manylocalmotions,index) \
    ((LocalMotions*)vs_vector_get(manylocalmotions,index))


/// stores local motions to file
int vsStoreLocalmotions(FILE* f, const LocalMotions* lms);

/// restores local motions from file
LocalMotions vsRestoreLocalmotions(FILE* f);


/// writes the header to the file that is to be holding the local motions
int vsPrepareFile(const VSMotionDetect* td, FILE* f);

/// appends the given localmotions to the file
int vsWriteToFile(const VSMotionDetect* td, FILE* f, const LocalMotions* lms);

/// reads the header of the file and return the version number (used by readLocalmotionsFile)
int vsReadFileVersion(FILE* f);

/*
 * reads the next set of localmotions from the file, return VS_ERROR on error or
 * if nothing is read (used by readLocalmotionsFile)
 */
int vsReadFromFile(FILE* f, LocalMotions* lms);

/*
 * reads the entire file of localmotions, return VS_ERROR on error or if nothing is read
 *
 *  The format is as follows:
 *   The file must begin with 'VID.STAB version\n'
 *   Lines with # at the beginning are comments and will be ignored
 *   Data lines have the structure: Frame NUM (<LocalMotions>)
 *   where LocalMotions ::= List [(LM v.x v.y f.x f.y f.size contrast match),...]
 */
int vsReadLocalMotionsFile(FILE* f, VSManyLocalMotions* lms);

// read the transformations from the given file (Deprecated format)
int vsReadOldTransforms(const VSTransformData* td, FILE* f , VSTransformations* trans);


#endif
