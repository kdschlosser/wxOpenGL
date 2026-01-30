# wxOpenGL
wxPython OpenGL framework

This project aims to make it easier to use OpenGL from Python using the wsPython 
cross platform GUI framework.

***WARNING***: Still in development

<br/>

Goals
_____

* ✅️ Child Window: OpenGL window as a child window so it can embedded into
                an application.
* ✅️️ OpenGL Context handling: Allows multiple OpenGL instances.
* ✅️ OpenGL Material handling: Wrappers that make dealing with OpenGL materials
                            easier to do.
* ⬜️ Movement/positioning: Built in mouse control that makes sense. 
* ✅️ Object containers: Objects are the things being rendered. This can be an entire 
                     scene or a single piece where groups would make up a scene.
* ✅️ Object selection: Ability to select an object

<br/>

***Supported 3d model formats***
________________________________
* STEP: Standard for the Exchange of Product Data (.stp, .step)
* VRML: Virtual Reality Modeling Language (.wrl)
* IGES: Initial Graphics Exchange Specification (.igs, .iges)
* AMF: Additive manufacturing file format (.amf)
* 3DS: 3D Studio Max 3DS (.3ds)
* AC: AC3D (.ac, .ac3d) 
* ASE: 3D Studio Max ASE (.ase)
* ASSBIN: Allegorithmic Substance Painter Scene within Document (.assbin)
* B3D: OpenBVE 3D (.b3d)
* BVH: Biovision BVH (.bvh) 
* COLLADA: Collada (.dae, .xml)
* DXF: AutoCAD DXF (.dxf) 
* CSM: CharacterStudio Motion ( .csm ) 
* HMP: 3D GameStudio Terrain ( .hmp ) 
* IRRMESH: Irrlicht Mesh (.irrmesh, .xml) 
* IQM: Inter-Quake Model (.iqm) 
* IRR: Irrlicht Scene (.irr, .xml) 
* LWO: LightWave Model ( .lwo ) 
* LWS: LightWave Scene ( .lws ) 
* MD2: Quake II (.md2) 
* MD3: Quake III (.md3) 
* MD5: Doom 3 (.md5mesh, .md5anim, .md5camera) 
* MDC: RtCW (.mdc) 
* MDL: Quake I (.mdl), 3D GameStudio Model ( .mdl )
* NFF: Neutral File Format (.nff), Sense8 WorldToolkit (.nff)
* NDO: 3D Low-polygon Modeler (.ndo)
* OFF: Object File Format (.off) 
* OBJ: Wavefront OBJ format (.obj) 
* OGRE: Ogre ( .mesh.xml, .skeleton.xml, .material ) 
* OPENGEX: OpenGEX-Fomat (.ogex) 
* PLY: Polygon File Format/Stanford Triangle Format. (.ply)  
* MS3D: Milkshape 3D ( .ms3d ) 
* COB: TrueSpace (.cob, .scn) 
* BLEND: Blender (.blend)
* IFC: Industry Foundation Classes IFC2x3 TC1, IFC4 Add2 TC1, IFC4x1, IFC4x2, and IFC4x3 Add2 (.ifc) 
* XGL: RealityWave 3D polygonal mesh(.xgl)
* FBX: FBX-Format, as ASCII and binary (.fbx)
* Q3D: Quest3D (.q3d)
* Q3BSP: Quake 3 BSP (.pk3) 
* RAW: Raw Triangles (.raw) 
* SIB: Silo Model Format (.sib)
* SMD: Valve Model (.smd, .vta) 
* STL: Stereolithography (.stl)  
* TERRAGEN: Terragen Terrain ( .ter ) 
* 3D 
* X: DirectX 3D Graphics Format (legacy) (.x)
* X3D: Extensible 3D (.x3d, .x3db, x3dz, x3dbz)
* GLTF: GL Transmission Format (.gltf, .glb)
* 3MF: 3D Manufacturing Format (.3mf) 
* MMD: MikuMikuDance Format (.pmd, .pmx)



***How the control works...***
______________________________

* Left mouse click and drag is look up/down and left/right
* Right mouse click and drag is move up/down  and sidestep left/right. 
  The focal point moves with the camera.
* Middle click and drag has a fixed focal point and the camera move around that point.
* Left click on an object will select it. The object will become translucent and glow blue.
  To deselect the object either you need to left click on the same object or left click 
  on a different object. You have the ability to move around with the object staying selected. 
* Mouse wheel walks forwards and backwards.
* Left click and drag an object when it is selected will move the object. I got crafty
  with the mechanics opn this because almost every 3D CAD stiyle program I have used has
  always had an object move erraticaly when moving using the mouse. So what I did to solve 
  that problem is an axis lock. The axis lock occurs when you first move the mouse.
  Make sure to move the mouse in the direction you want to move the object and it will then
  lock to moving on that axis. The lock gets released only when you release the mouse button.
  the object will stay selected after releasing the mouse button. I set it up like this so 
  direction changes are simple to do.
* Right click and drag on a selected object will rotate the object. The control function in 
  the same manner with the rotation being locked to a specific axis once you move the mouse.
  > NOTE: This feature I am still working on and it does not function properly at the time being.



***Extra features***
____________________

There is a mechanism that I built in that holds config settings. This mechanism
stores the config settings in a sqlite3 database. By default the database is created
in memory so the setting are not persistanct between reloads of the library. You can provide
a path to save the settings to file so it will be persistant. Currently the config settings 
are shared if you have more than one instance of the library running. I will be making some
changes to the settings to allow for separate settings for each instance that is running.

Here are the config settings...

'''
* ground_height (default: `0.0`): Sets where the "floor" is located.
                                This is the bottom limit of object positioning 
                                and also how low the camera is able to move.
         
* eye_height (default `10.0`): Starting height of the camera. This setting is not being used yet.
* reflections (default `False`): Show reflections on the floor. `grid.render` must also be set 
                                 to `True`. This is not being used yet.
* reflection_strength (default `50.0`): Range is 0.0 - 100.0. This is how strong the reflection is.
                                      Not being used yet.   

* grid: Grid settings
  * render (defualt `True`): Turn on and off rendering the grid floor. The impact to performance for 
                             rendering the floor is very small. There is a startup time penatly of 
                             about 7ms. The floor gets build and then stored into the memory on the 
                             video card which makes it super fast to render when a refresh occurs. 
                             I am talking 0.13ms fast.  
  * size (default `1000`): This is how far the floor goes in all directions. The clipping plane
                           for far is hard coded at 1000. so the floor is defulted to that clipping 
                           distance. The floow distance is measure as 1000 from `(0, ground_height, 0)`
                           that means the total flore area has a size of `(2000, 2000)`.
  * step (default `50`): This is the size of the checkerboard. Like the `size` this is a 1/2 value so 
                         setting it to 50 produces squares that have a size of `(100, 100)` 

  * odd_color (default `[0.3, 0.3, 0.3, 0.8]`): Odd square color. This is a scalar value for 
                                                `[red, green, blue, alpha]`
                                                each component has a range of `0.0` to `1.0`
  * even_color (default `[0.8, 0.8, 0.8, 0.8]`): Even square colors. Works the same as the `odd_color`
                                                 setting.

* virtual_canvas: One of the things I did not care for was resizing the window and having
                  the objects in view change viewable size. I wanted to keep the appearance the same
                  and increase the field of view when making the window larger or smaller.
                  This was a but tricky to do because I had to wrap the OpenGL window with a `wx.Panel`
                  and the gl window is not coupled to a sizer. The gl window is always the same size
                  and the panel that holds the gl window is what clips the view.
                  
  * width (default `1920`): Sets the width of the gl window. If you need to change
                            this setting you will want to keep the aspect ratio of 16:9
                            between the width and height otherwise things can get distored. 
  * height (defualt `1080`): Sets the height, same rules apply that are outlined above. 

    class movement(metaclass=_Config):
        angle_detent = 10.0
        move_detent = 5.0

        angle_snap = -1
        move_snap = -1

    class keyboard_settings(metaclass=_Config):
        max_speed_factor = 10.0
        speed_factor_increment = 0.1
        start_speed_factor = 1.0

    class rotate(metaclass=_Config):
        mouse = MOUSE_MIDDLE
        up_key = ord('w')
        down_key = ord('s')
        left_key = ord('a')
        right_key = ord('d')
        sensitivity = 0.4

    class pan_tilt(metaclass=_Config):
        mouse = MOUSE_LEFT
        up_key = ord('o')
        down_key = ord('l')
        left_key = ord('k')
        right_key = ord(';')
        sensitivity = 0.2

    class truck_pedestal(metaclass=_Config):
        mouse = MOUSE_RIGHT
        up_key = ord('8')
        down_key = ord('2')
        left_key = ord('4')
        right_key = ord('6')
        sensitivity = 0.2
        speed = 1.0

    class walk(metaclass=_Config):
        mouse = MOUSE_WHEEL | MOUSE_SWAP_AXIS
        forward_key = wx.WXK_UP
        backward_key = wx.WXK_DOWN
        left_key = wx.WXK_LEFT
        right_key = wx.WXK_RIGHT
        sensitivity = 1.0
        speed = 5.0

    class zoom(metaclass=_Config):
        mouse = MOUSE_NONE  # | MOUSE_REVERSE_WHEEL_AXIS
        in_key = wx.WXK_ADD
        out_key = wx.WXK_SUBTRACT
        sensitivity = 5.0

    class reset(metaclass=_Config):
        key = wx.WXK_HOME
        mouse = MOUSE_NONE

    class debug:
        log_args = False
        call_duration = False
        bypass = True

'
