from agno.playground import Playground

from demo.agents import ResearchGoalClarificationAgentBuilder


agent = ResearchGoalClarificationAgentBuilder().build_agent()
playground = Playground(agents=[agent])

app = playground.get_app()

if __name__ == "__main__":
    playground.serve(app="run_demo:app", reload=True)
