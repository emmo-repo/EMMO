Installing the FaCT++ reasoner plugin for Protégé 5.5.0 on Windows
==================================================================
There is a known issue with the FaCT++ reasoner for Protégé 5.5.0 on Windows.
Fortunately a solution has been posted on http://protege-project.136.n4.nabble.com/Protege-5-5-0-and-Fact-td4671904.html.

Instructions
------------
1. Download [OpenJDK](https://jdk.java.net/13/) and extract the zip file.
2. Download the [FaCT++ plugin](https://bitbucket.org/dtsarkov/factplusplus/downloads/uk.ac.manchester.cs.owl.factplusplus-P5.x-v1.6.5.jar) and save it in the Protégé plugin directory.
3. Download the [fix](https://gist.githubusercontent.com/jpi-seb/12627bba6509a85a9c75afd262e78469/raw/28016a4b292c94549623c71dff4028cbea274a29/factplusplus-P5.x-v1.6.5-manifest-fix-win10.txt) to the same directory.
4. Open a command window in the plugin directory and run

```Shell Session
/path/to/jdk-13.0.1/bin/jar umf factplusplus-P5.x-v1.6.5-manifest-fix-win10.txt uk.ac.manchester.cs.owl.factplusplus-P5.x-v1.6.5.jar
```

5. Open Protégé and check that FaCT++ can be found under the Reasoner menu.
