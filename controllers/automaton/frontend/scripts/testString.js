async function testString(autId, testStrings) {
  // Base URL of the API
  const BASE_URL = "http://localhost:8000";

  // Data to create the automaton
  const createAutomatonData = {
    aut_id: autId,
    alph: ["a", "b", "c"],
    Q: ["q0", "q1", "q2"],
    F: ["q2"],
    q0: "q0",
  };

  // Asynchronous function to handle the creation and testing process
  (async () => {
    try {
      // Create the automaton
      const createResponse = await fetch(
        `${BASE_URL}/create/${createAutomatonData.aut_id}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(createAutomatonData),
        }
      );

      if (!createResponse.ok) throw new Error(await createResponse.text());
      const createData = await createResponse.json();
      console.log("Automaton created successfully:", createData);

      // List of transitions to add
      const transitions = [
        { char: "a", state_from: "q0", state_to: "q0" },
        { char: "b", state_from: "q0", state_to: "q1" },
        { char: "b", state_from: "q1", state_to: "q1" },
        { char: "c", state_from: "q1", state_to: "q2" },
        { char: "c", state_from: "q2", state_to: "q2" },
      ];

      for (const transition of transitions) {
        const transitionResponse = await fetch(
          `${BASE_URL}/automata/${createAutomatonData.aut_id}/add_transition`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(transition),
          }
        );

        if (!transitionResponse.ok)
          throw new Error(await transitionResponse.text());
        const transitionData = await transitionResponse.json();
        console.log(
          `Transition ${JSON.stringify(transition)} added successfully:`,
          transitionData
        );
      }

      // Strings to test
      const stringsToTest = testStrings;
      for (const string of stringsToTest) {
        const testResponse = await fetch(
          `${BASE_URL}/automata/${createAutomatonData.aut_id}/test/${string}`
        );

        if (!testResponse.ok) throw new Error(await testResponse.text());
        const testData = await testResponse.json();
        console.log(
          `String '${string}' test result:`,
          JSON.stringify(testData, null, 4)
        );
      }
    } catch (error) {
      console.error("Error:", error);
    }
  })();
}


testString("Autom", ["aabbbc"])