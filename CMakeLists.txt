##
# CMakeLists.txt
#
# Copyright 2015 Fabian Wenzelmann
#
# This file is part of Recognition-Procedures-for-Boolean-Functions.
#
# Recognition-Procedures-for-Boolean-Functions is free software: you
# can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Recognition-Procedures-for-Boolean-Functions is distributed in the hope
# that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Recognition-Procedures-for-Boolean-Functions.
#
# If not, see <http://www.gnu.org/licenses/>.
##

cmake_minimum_required (VERSION 2.8) 
project(BFR)

set(CMAKE_CXX_COMPILER_INIT g++)
# TODO: not really nice (set it for other compilers?), but required...
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
link_directories("${BFR_SOURCE_DIR}/obj")

set(Boost_USE_STATIC_LIBS  ON)
find_package(Boost COMPONENTS system filesystem date_time REQUIRED)
             
SET(CMAKE_BUILD_TYPE Release)
#SET(CMAKE_BUILD_TYPE Debug)

SET(COMMON_INCLUDES
	"${BFR_SOURCE_DIR}/src"
    "${BFR_SOURCE_DIR}/include")

include_directories(
	${COMMON_INCLUDES}
)
    
add_subdirectory (obj)

SET(COMMON_LIBRARIES
	"bfr"
	${Boost_FILESYSTEM_LIBRARY}
    ${Boost_SYSTEM_LIBRARY}
	# remove it on non-linux systems?
	"dl"
)
	

add_executable(boolean-function-recognition ${BFR_SOURCE_DIR}/src/BFRMain.cpp)
target_link_libraries(boolean-function-recognition ${COMMON_LIBRARIES})


# tests
ENABLE_TESTING()
add_subdirectory (tests)

SET(BFR_VERSION "0.9.1")
SET(DOXYGEN_OUT_DIR "${BFR_SOURCE_DIR}/doc")
SET(DOXYGEN_INCLUDE "${BFR_SOURCE_DIR}/include")
SET(DOXYGEN_IMAGE_PATH "${BFR_SOURCE_DIR}/images")
SET(DOXYGEN_STYLE_PATH "${BFR_SOURCE_DIR}/doxy_style")

add_subdirectory (images)

# Doxygen target
find_package(Doxygen)
if(DOXYGEN_FOUND)
configure_file(${BFR_SOURCE_DIR}/Doxyfile.in ${BFR_BINARY_DIR}/Doxyfile @ONLY)
add_custom_target(doc
${DOXYGEN_EXECUTABLE} ${BFR_BINARY_DIR}/Doxyfile
WORKING_DIRECTORY ${BFR_BINARY_DIR}
COMMENT "Generating documentationg with Doxygen." VERBATIM
)
endif(DOXYGEN_FOUND)
