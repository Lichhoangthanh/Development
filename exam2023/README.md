# webdev-lab-5


<p class="mt-4 ms-4">{{ post.text }}</p>
      
        <div class="container mb-5 mt-5">
                  <div class="col-md-12 ">
                    {% for comment in post.comments %}
                    <div class="media mt-5">
                      <img
                        class="mr-3 rounded-circle"
                        alt="Bootstrap Media Preview"
                        src="https://jola.vn/Article/ruIISDjqw/910-maxresdefault.jpg"
                        width="50"
                        height="50"
                      />
                      <div class="media-body">
                        <div class="row">
                          <div class="col-8 d-flex">
                            <h5>{{comment.author}}</h5>
                            <span>- 2 hours ago</span>
                          </div>

                          <div class="col-4">
                            <div class="pull-right reply">
                              <a href="#"
                                ><span
                                  ><i class="fa fa-reply"></i> reply</span
                                ></a
                              >
                            </div>
                          </div>
                        </div>
                        {{comment.text}} {% for reply in comment.replies %}
                        <div class="media mt-5 ms-5">
                          <a class="pr-3" href="#"
                            ><img
                              class="rounded-circle"
                              alt="image"
                              src="https://jola.vn/Article/ruIISDjqw/910-maxresdefault.jpg"
                              width="50"
                              height="50"
                          /></a>
                          <div class="media-body">
                            <div class="row">
                              <div class="col-12 d-flex">
                                <h5>{{reply.author}}</h5>
                                <span>- 3 hours ago</span>
                              </div>
                            </div>
                            {{reply.text}}
                          </div>
                          {% endfor %}
                        </div>
                      </div>
                    </div>
                    {% endfor %}
                  </div>
                
              
      <div class="py-3 border-0" style="background-color: #f8f9fa">
        <div class="d-flex flex-start w-100">
          <img
            class="rounded-circle shadow-1-strong me-3"
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDrFK8jqytGxBolyLVII44H_jzzBL_vM3wJKenPzPU8A&s"
            alt="avatar"
            width="50"
            height="50"
          />
          <div class="form-outline w-100">
            <textarea
              placeholder="Message"
              class="form-control"
              id="textAreaExample"
              rows="4"
              style="background: #fff"
            ></textarea>
          </div>
        </div>
        <div class="text-center mt-2 pt-1">
          <button type="button" class="btn btn-primary btn-sm">
            Post comment
          </button>
          <button type="button" class="btn btn-outline-primary btn-sm">
            Cancel
          </button>
        </div>
      </div>