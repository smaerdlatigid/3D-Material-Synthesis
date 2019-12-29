using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class screenCapture : MonoBehaviour
{
    public GameObject light;
    public GameObject surface; 
    public Material material;
    public GameObject directional; 
    public List<GameObject> lights; 
    public float[] yAngles = {90,210,330};

    Vector3 pos; 
    GameObject obj;
    float r,h;
    Light lt;

    private Texture2D[] textures;
    
    void Start()
    {
        textures = Resources.LoadAll<Texture2D>("Textures");
        Debug.Log(textures.Length);
        Debug.Log(textures[0].name);
        Debug.Log(textures[1].name);
        material.SetTexture("_BaseMap", textures[0]);
        material.SetTexture("_BumpMap", textures[1]);

        lights = new List<GameObject>();
        lights.Add(light);

        for(int y=0; y<yAngles.Length; y++)
        {
            // Instatiate point sources
            h = light.transform.position.y * 0.35f;
            r = h * Mathf.Tan(2 * 3.14159f * 30 / 360f); // tripod angle 
            pos = new Vector3(
                r * Mathf.Cos(2 * 3.14159f * yAngles[y] / 360f),
                light.transform.position.y - h, 
                r * Mathf.Sin(2*3.14159f*yAngles[y]/360f)
            );
            pos += surface.transform.position;
            obj = Instantiate(light, pos, Quaternion.identity);
            obj.SetActive(false);
            lights.Add(obj);
            lt = obj.GetComponent<Light>();
            lt.intensity = 0.1f;

            // Instatiate directional light
            /*
            Euler angles to Qauter
            (45,0,0)
            (135,0,0)
            (45,90,0)
            (45,-90,0)
            */
        }
        capturing = false;
        DisablePointSources();
        // Create list of training images
    }

    void DisablePointSources()
    {
        for (int i = 0; i < lights.Count; i++)
        {
            lights[i].SetActive(false);
        }
    }

    public string filepath = "C:\\Users\\Kyle\\Programs\\github\\PhotoMaterialSynthesis\\TensorFlow\\train\\UnitySamples";
    string filename;
    bool capturing = false;
    int ti = 0;
    int augmentations = 50;
    int ai = -1;

    IEnumerator CaptureSequence()
    {
        DisablePointSources();
        directional.SetActive(false);

        for (int i = 0; i < lights.Count; i++)
        {
            lights[i].SetActive(true);
            filename = string.Format("{0}\\texture_{1}_{2}_color{3}.png", filepath, ti, ai, i.ToString());
            ScreenCapture.CaptureScreenshot(filename);
            yield return new WaitForSeconds(0.25f); 
            Debug.Log(filename+" captured.");
            lights[i].SetActive(false);
        }

        // Turn on Directional
        directional.SetActive(true);
        filename = string.Format("{0}\\texture_{1}_{2}_color{3}.png", filepath, ti, ai, 0);
        ScreenCapture.CaptureScreenshot(filename);
        yield return new WaitForSeconds(0.25f);

        // change albedo to normal map
        material.SetTexture("_BaseMap", textures[2*ti+1]);
        material.SetTexture("_BumpMap", null);
        filename = string.Format("{0}\\texture_{1}_{2}_normal.png", filepath, ti, ai);
        ScreenCapture.CaptureScreenshot(filename);

        yield return new WaitForSeconds(0.25f);
        Debug.Log("Done Capturing");
        capturing=false;
    }
    Vector2 offset, scale;
    void Update()
    {
        if (capturing)
        {
            
        }
        else
        {
            if (ti<textures.Length/2){
                ai += 1; 
                if (ai >= augmentations)
                {
                    ai = 0;
                    ti +=1;
                }
                material.SetTexture("_BaseMap", textures[2*ti]);
                material.SetTexture("_BumpMap", textures[2*ti+1]);
                material.SetFloat("_BumpScale", 1f);
                offset = new Vector2(Random.value, Random.value);
                scale = new Vector2(0.5f * Random.value + 0.75f, 0.5f * Random.value + 0.75f);
                material.SetTextureOffset("_BaseMap",offset);
                material.SetTextureScale("_BaseMap",scale);
                material.SetTextureOffset("_BumpMap", offset);
                material.SetTextureScale("_BumpMap", scale);
                StartCoroutine(CaptureSequence());
                capturing = true;
            }
        }
    }
    
    /******************************************************************/
}
