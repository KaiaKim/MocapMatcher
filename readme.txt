Kaia Mocap Matcher
==================

English
-------

Installation:
1. Extract the entire Kaia_MocapMatcher folder from the zip.
2. In Maya, drag and drop install.mel into the Maya window.
3. A MocapMatcher button will be added to the current shelf.
4. Click the shelf button to open the tool.
5. Keep the MocapMatcher subfolder next to install.mel. Do not move files
   out of the subfolder.

Usage:
1. Set the Origin Jnts namespace using the text field or "detect from
   selected".
2. Set the Target Ctrls namespace the same way.
3. Expand "Origin Jnts / Target Ctrls" if you need to edit a name.
4. Click "1: Create Locators".
5. Click "2: Attach Locs to Origin Jnts".
6. Click "3: Attach Target Ctrls to Locs".
7. Click "4: Bake".

The current version uses Advanced Skeleton joints as origin joints and
Advanced Skeleton controllers as target controls. Namespace values are
cached locally in MocapMatcher/namespace_cache.json.


Kaia Mocap Matcher
==================

한국어
------

설치 방법:
1. zip 파일의 Kaia_MocapMatcher 폴더 전체를 압축 해제합니다.
2. Maya에서 install.mel 파일을 Maya 창으로 드래그 앤 드롭합니다.
3. 현재 선택된 Shelf에 MocapMatcher 버튼이 추가됩니다.
4. Shelf 버튼을 클릭하여 툴을 실행합니다.
5. install.mel과 MocapMatcher 폴더는 같은 위치에 있어야 합니다.
   폴더 안의 파일을 다른 위치로 옮기지 마세요.

사용 방법:
1. Origin Jnts의 namespace를 입력하거나 "detect from selected" 버튼을
   사용합니다.
2. Target Ctrls의 namespace도 같은 방법으로 입력합니다.
3. 이름을 수정해야 하는 경우 "Origin Jnts / Target Ctrls"를 펼칩니다.
4. "1: Create Locators"를 클릭합니다.
5. "2: Attach Locs to Origin Jnts"를 클릭합니다.
6. "3: Attach Target Ctrls to Locs"를 클릭합니다.
7. "4: Bake"를 클릭합니다.

현재 버전은 Advanced Skeleton joint를 Origin Jnts로 사용하고,
Advanced Skeleton controller를 Target Ctrls로 사용합니다. Namespace
값은 MocapMatcher/namespace_cache.json에 로컬로 저장됩니다.
