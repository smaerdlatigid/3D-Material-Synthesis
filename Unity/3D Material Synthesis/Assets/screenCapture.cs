using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class screenCapture : MonoBehaviour
{
    public GameObject light;
    public GameObject surface; 
    public Material material;
    public List<GameObject> lights; 

    Vector3[] angles = {
        new Vector3(35,0,0),
        new Vector3(-35,0,0),
        new Vector3(0,35,0),
        new Vector3(0,-35,0)
    };

    Vector3 pos; 
    Quaternion rot; 

    GameObject obj;
    Light lt;

    private Texture2D[] textures;
    
    void Start()
    {
        textures = Resources.LoadAll<Texture2D>("Textures");
        Debug.Log(textures.Length);
        material.SetTexture("_BaseMap", textures[0]);
        material.SetTexture("_BumpMap", textures[1]);

        lights = new List<GameObject>();
        lights.Add(light);

        for (int a=0; a<angles.Length; a++)
        {
            rot = Quaternion.Euler(angles[a]);
            obj = Instantiate(light,light.transform.position, rot);
            obj.SetActive(false);
            lights.Add(obj);
        }
        capturing = false;
        DisableLightSources();
    }

    void DisableLightSources()
    {
        for (int i = 0; i < lights.Count; i++)
        {
            lights[i].SetActive(false);
        }
    }

    public string filepath = "C:\\Users\\Kyle\\Programs\\github\\PhotoMaterialSynthesis\\TensorFlow\\test\\UnitySamples";
    string filename;
    bool capturing = false;
    int ti = 0;
    int augmentations = 2;
    int ai = -1;

    IEnumerator CaptureSequence()
    {
        DisableLightSources();

        surface.transform.rotation = Quaternion.Euler(0, 0, Random.value * 90);
        for (int i = 0; i < lights.Count; i++)
        {
            lights[i].SetActive(true);
            filename = string.Format("{0}\\texture{1}_{2}_color{3}.png", filepath, ti, ai, i.ToString());
            ScreenCapture.CaptureScreenshot(filename);
            yield return new WaitForSeconds(0.25f); 
            Debug.Log(filename+" captured.");
            lights[i].SetActive(false);
        }

        // change albedo to normal map
        lights[0].SetActive(true);
        material.SetTexture("_BaseMap", textures[2*ti+1]);
        material.SetTexture("_BumpMap", null);
        filename = string.Format("{0}\\texture{1}_{2}_normal.png", filepath, ti, ai);
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
            if (ti<textures.Length/2-1){
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
}
