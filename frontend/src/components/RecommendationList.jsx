
import RecommendationCard from "./RecommendationCard";


function RecommendationList({ recommendations }) {

  if (!recommendations) {
    return null;
  }


  if (recommendations.length === 0) {

    return (
      <p>
        No suitable movies found.
      </p>
    );
  }


  return (

    <section className="recommendation-list">

      <h2>
        Recommendations
      </h2>


      <div className="recommendation-grid">

        {recommendations.map(
          (movie, index) => (

            <RecommendationCard
              key={movie.title}
              movie={movie}
              index={index}
            />

          )
        )}

      </div>

    </section>
  );
}


export default RecommendationList;