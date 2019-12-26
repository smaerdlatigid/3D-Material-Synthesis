using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class screenCapture : MonoBehaviour
{
    public GameObject light;
    public GameObject surface; 
    public Material material;

    public List<GameObject> lights; 

    public float[] yAngles = {90,210,330};

    Vector3 pos; 
    GameObject obj;
    float r,h;
    Light lt;
    
    void Start()
    {
        lights = new List<GameObject>();
        lights.Add(light);

        // instantiate a bunch of lights 
        for(int y=0; y<yAngles.Length; y++)
        {
            // Instatiate gameObject
            h = light.transform.position.y * 0.5f;
            r = h * Mathf.Tan(2 * 3.14159f * 35 / 360f); // tripod angle 
            pos = new Vector3(
                r * Mathf.Cos(2 * 3.14159f * yAngles[y] / 360f),
                h, 
                r * Mathf.Sin(2*3.14159f*yAngles[y]/360f)
            );
            pos += surface.transform.position;
            obj = Instantiate(light, pos, Quaternion.identity);
            // obj.transform.SetParent(light.transform);
            obj.SetActive(false);
            lights.Add(obj);
            lt = obj.GetComponent<Light>();
            lt.intensity = 0.1f; 
        }

        // Create list of training images
    }

    void Update()
    {
        // loop through training materials
        // loop through point lights and capture
        // turn on directional light, switch albedo to normal map, capture "truth"
    }
}
