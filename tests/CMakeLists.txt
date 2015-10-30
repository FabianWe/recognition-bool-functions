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

find_package(GTest)
if (GTEST_FOUND)
include_directories(${GTEST_INCLUDE_DIRS}
)

SET(TEST_LINK_LIBRARIES
	${COMMON_LIBRARIES}
	${GTEST_BOTH_LIBRARIES}
	"pthread"
)

SET(TEST_NAMES
)

SET(TEST_BIN "${CMAKE_BINARY_DIR}/tests")

# copy the test files
file(COPY ${BFR_SOURCE_DIR}/tests/test_files DESTINATION "${TEST_BIN}")

# add exectuables
foreach(arg ${TEST_NAMES})
	add_executable("${arg}Test" "${BFR_SOURCE_DIR}/tests/${arg}Test.cpp")
	target_link_libraries("${arg}Test" ${TEST_LINK_LIBRARIES})
	add_test("${arg}" "${TEST_BIN}/${arg}Test")
endforeach(arg)

else (GTEST_FOUND)
MESSAGE(STATUS "Can't find goole test libraries.")
endif (GTEST_FOUND)
