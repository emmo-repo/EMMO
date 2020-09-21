Setting up Protégé for working with EMMO-based ontologies
=========================================================
After you have installed Protégé (can be downloaded from
[https://protege.stanford.edu/products.php#desktop-protege](https://protege.stanford.edu/products.php#desktop-protege))
it is recommended that you go through the following steps:

  * To render by label, select `View -> 'Render by annotation property' -> skos:prefLabel`

  * Install the FaCT++ reasoner:
      1. Select `File -> 'Check for plugins...'`
      2. Tick off for the FaCT++ reasoner
      3. Click `Install`
      4. Restart Protégé

    On Windows, there is a known issue with FaCT++ for Protégé 5.5.0.  See
    [these instructions](installing_factplusplus.md) for how to resolve it.

  * Preferences for setting up new entities:
      1. Select `File -> Preferences...`
      2. Select the "New entities" tab
      3. Under **Entity IRI** tick for
        - Start with: `Active ontology IRI`
        - Followed by: `#`
        - End with: `Auto-generated ID` select
      4. Under **Entity Label**
        - Tick for `Same as label renderer`
      5. Under **Auto-generated ID**
        - Tick for `Globally unique`
        - Set prefix to "EMMO_"

    Below is a screenshot of how it should look like.

    ![Preferences for new entities in Protégé.](new_entities.png)
