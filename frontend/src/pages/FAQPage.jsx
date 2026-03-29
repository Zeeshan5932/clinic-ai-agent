function FAQPage() {
  return (
    <section className="page-stack">
      <div className="page-title">
        <h1>Clinic Information</h1>
        <p>Frequently requested details for VitaPulse Clinic patients.</p>
      </div>

      <div className="faq-grid">
        <article className="card">
          <h3>Working Hours</h3>
          <p>Mon-Sat 10AM-8PM</p>
        </article>

        <article className="card">
          <h3>Phone</h3>
          <p>+92 300 1234567</p>
        </article>

        <article className="card">
          <h3>Email</h3>
          <p>hello@vitapulseclinic.com</p>
        </article>

        <article className="card">
          <h3>Address</h3>
          <p>Okara</p>
        </article>
      </div>
    </section>
  );
}

export default FAQPage;
